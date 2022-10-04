from datetime import datetime as dt

from django.contrib.auth import get_user_model
from django.db.models import Exists, F, OuterRef, Sum, Value
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters import rest_framework as filters

from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import (HTTP_201_CREATED, HTTP_204_NO_CONTENT)
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from recipes.models import (Favorite, Ingredient, IngredientAmount, Recipe,
                            ShoppingCart, Tag)

from .filters import IngredientSearchFilter, RecipeFilter
from .permissions import AdminOrReadOnly, AuthorAdminOrReadOnly
from .serializers import (IngredientSerializer, RecipeListSerializer,
                          RecipeWriteSerializer, TagSerializer)

User = get_user_model()


class TagViewSet(ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (AdminOrReadOnly,)
    pagination_class = None


class IngredientViewSet(ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (AdminOrReadOnly,)
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = IngredientSearchFilter
    search_fields = ('^name',)
    pagination_class = None


class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all().order_by('id')
    permission_classes = (AuthorAdminOrReadOnly,)
    pagination_class = PageNumberPagination
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def get_queryset(self):
        self.paginator.page = self.request.query_params.get("page", 1)
        self.paginator.page_size = self.request.query_params.get("limit", 6)

        is_favorited = True if self.request.query_params.get(
            "is_favorited", '0') == '1' else False
        is_in_shopping_cart = True if self.request.query_params.get(
            "is_in_shopping_cart", '0') == '1' else False

        if self.request.user.is_anonymous:
            qs = Recipe.objects.all().order_by('id')
            qs = qs.annotate(
                is_favorited=Value(False),
                is_in_shopping_cart=Value(False)
            )
        else:
            favorite_qs = Favorite.objects.filter(
                user=self.request.user, recipe=OuterRef('id')
            )
            cart_qs = ShoppingCart.objects.filter(
                user=self.request.user, recipe=OuterRef('id')
            )
            qs = Recipe.objects.all().order_by('id').annotate(
                is_favorited=Exists(favorite_qs),
                is_in_shopping_cart=Exists(cart_qs)
            )
            if is_favorited:
                qs = qs.filter(
                    id__in=(favorite_qs.values('recipe_id'))
                )
            if is_in_shopping_cart:
                qs = qs.filter(
                    id__in=(cart_qs.values('recipe_id'))
                )
        return qs

    def get_serializer_class(self):
        if self.request.method in ('GET'):
            return RecipeListSerializer
        return RecipeWriteSerializer

    @staticmethod
    def post_method(request, pk, serializers):
        data = {'user': request.user.id, 'recipe': pk}
        serializer = serializers(data=data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=HTTP_201_CREATED)

    @staticmethod
    def delete_method(request, pk, model):
        user = request.user
        recipe = get_object_or_404(Recipe, id=pk)
        model_obj = get_object_or_404(model, user=user, recipe=recipe)
        model_obj.delete()
        return Response(status=HTTP_204_NO_CONTENT)

    @action(
        methods=['POST'],
        url_path='favorite',
        detail=True,
        permission_classes=[IsAuthenticated]
    )
    def favorite(self, request, pk):
        recipe = get_object_or_404(Recipe, id=pk)
        favotite = Favorite.objects.create(
            user=request.user,
            recipe=recipe)
        favotite.save()
        data = {
            "id": favotite.recipe.pk,
            "name": favotite.recipe.name,
            "image": favotite.recipe.image.url,
            "cooking_time": favotite.recipe.cooking_time
        }
        return Response(data, status=HTTP_201_CREATED)

    @favorite.mapping.delete
    def delete_favorite(self, request, pk):
        self.delete_method(
            request=request, pk=pk, model=Favorite)
        return Response(status=HTTP_204_NO_CONTENT)

    @action(
        methods=['POST'],
        url_path='shopping_cart',
        detail=True,
        permission_classes=[IsAuthenticated])
    def shopping_cart(self, request, pk):
        recipe = get_object_or_404(Recipe, id=pk)
        cart = ShoppingCart.objects.create(
            user=request.user,
            recipe=recipe)
        cart.save()
        data = {
            "id": cart.recipe.pk,
            "name": cart.recipe.name,
            "image": cart.recipe.image.url,
            "cooking_time": cart.recipe.cooking_time
        }
        return Response(data, status=HTTP_201_CREATED)

    @shopping_cart.mapping.delete
    def delete_shopping_cart(self, request, pk):
        self.delete_method(
            request=request, pk=pk, model=ShoppingCart)
        return Response(status=HTTP_204_NO_CONTENT)

    @action(
        methods=['GET'],
        url_path='download_shopping_cart',
        detail=False,
        permission_classes=(IsAuthenticated,)
    )
    def download_shopping_cart(self, request):
        user = self.request.user
        if user.is_anonymous:
            return Response(status=403)

        cart_qs = ShoppingCart.objects.filter(
            user=self.request.user, recipe=OuterRef('id')
        )
        qs = Recipe.objects.all().filter(
            id__in=(cart_qs.values('recipe_id'))
        )
        ingredients = IngredientAmount.objects.filter(
            recipe__in=(qs.values('id'))
        ).values(
            ingredient=F('ingredients__name'),
            measure=F('ingredients__measurement_unit')
        ).annotate(amount=Sum('amount'))

        filename = f'{user.first_name}_shopping_list.txt'
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
