from datetime import datetime as dt
from urllib.parse import unquote

from django.contrib.auth import get_user_model
from django.db.models import F, Sum
from django.http.response import HttpResponse
from djoser.views import UserViewSet as DjoserUserViewSet
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from recipes.models import Ingredient, IngredientAmount, Recipe, Tag

from .mixins import AddDelViewMixin
from .permissions import AdminOrReadOnly, AuthorAdminOrReadOnly
from .serializers import (GetRecipeSerializer, IngredientSerializer,
                          RecipeSerializer, TagSerializer,
                          UserSubscribeSerializer)

User = get_user_model()


class UserViewSet(DjoserUserViewSet, AddDelViewMixin):
    pagination_class = PageNumberPagination
    serializer_class = UserSubscribeSerializer

    @action(methods=('get', 'add', 'delete',), detail=True)
    def subscribe(self, id):
        return self.add_del_obj(id, 'subscribe')

    @action(methods=('get',), detail=False)
    def subscription(self, request):
        user = self.request.user
        if user.is_anonymous:
            return Response(status=HTTP_401_UNAUTHORIZED)
        all_authors = user.subscribe.all()
        pages = self.paginate_queryset(all_authors)
        serializer = UserSubscribeSerializer(
            pages, many=True, context={'request': request}
        )
        return self.get_paginated_response(serializer.data)


class TagViewSet(ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (AdminOrReadOnly,)


class IngredientViewSet(ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (AdminOrReadOnly,)

    def get_queryset(self):
        name = self.request.query_params.get('name')
        queryset = self.queryset
        if name:
            if name[0] == '%':
                name = unquote(name)
            else:
                name = name.translate(str.maketrans(
                    'qwertyuiop[]asdfghjkl;\'zxcvbnm,./',
                    'йцукенгшщзхъфывапролджэячсмитьбю.'
                    ))
            name = name.lower()
            start_queryset = list(queryset.filter(name__startswith=name))
            contain_queryset = queryset.filter(name__contains=name)
            start_queryset.extend(
                [i for i in contain_queryset if i not in start_queryset]
            )
            queryset = start_queryset
        return queryset


class RecipeViewSet(ModelViewSet, AddDelViewMixin):
    queryset = Recipe.objects.select_related('author')
    serializer_class = RecipeSerializer
    permission_classes = (AuthorAdminOrReadOnly,)
    pagination_class = PageNumberPagination
    add_serializer = GetRecipeSerializer

    def get_queryset(self):
        queryset = self.queryset

        tags = self.request.query_params.getlist('tags')
        if tags:
            queryset = queryset.filter(
                tags__slug__in=tags).distinct()

        author = self.request.query_params.get('author')
        if author:
            queryset = queryset.filter(author=author)

        # Следующие фильтры только для авторизованного пользователя
        user = self.request.user
        if user.is_anonymous:
            return queryset

        is_in_shopping_cart = self.request.query_params.get(
            'is_in_shopping_cart'
            )
        if is_in_shopping_cart in ('1', 'true',):
            queryset = queryset.filter(cart=user.id)
        elif is_in_shopping_cart in ('0', 'false',):
            queryset = queryset.exclude(cart=user.id)

        is_favorited = self.request.query_params.get('is_favorited')
        if is_favorited in ('1', 'true',):
            queryset = queryset.filter(favorite=user.id)
        if is_favorited in ('0', 'false',):
            queryset = queryset.exclude(favorite=user.id)

        return queryset

    @action(methods=('get', 'add', 'delete',), detail=True)
    def favorite(self, request, pk):
        return self.add_del_obj(pk, 'favorite')

    @action(methods=('get', 'add', 'delete',), detail=True)
    def shopping_cart(self, request, pk):
        return self.add_del_obj(pk, 'shopping_cart')

    @action(methods=('get',), detail=False)
    def download_shopping_cart(self, request):
        user = self.request.user
        if not user.carts.exists():
            return Response(status=HTTP_400_BAD_REQUEST)
        ingredients = IngredientAmount.objects.filter(
            recipe__in=(user.carts.values('id'))
        ).values(
            ingredient=F('ingredients__name'),
            measure=F('ingredients__measurement_unit')
        ).annotate(amount=Sum('amount'))

        filename = f'{user.username}_shopping_list.txt'
        shopping_list = (
            f'Shopping_list for:\n\n{user.first_name}\n\n'
            f'{dt.now().strftime("%d/%m/%Y %H:%M")}\n\n'
        )
        for ing in ingredients:
            shopping_list += (
                f'{ing["ingredient"]}: {ing["amount"]} {ing["measure"]}\n'
            )

        shopping_list += '\n\nCounted in Foodgram'

        response = HttpResponse(
            shopping_list, content_type='text.txt; charset=utf-8'
        )
        response['Content-Disposition'] = f'attachment; filename={filename}'
        return response
