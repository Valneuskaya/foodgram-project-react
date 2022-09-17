from datetime import datetime as dt

from django.db.models import Exists, OuterRef
from django.contrib.auth import get_user_model
from django.db.models import F, Sum
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters import rest_framework as filters
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
)
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from api.filters import IngredientSearchFilter, RecipeFilter
from recipes.models import (
    Ingredient, IngredientAmount,
    Recipe, Tag, Favorite, ShoppingCart
)
from users.serializers import GetRecipeSerializer

from .permissions import AdminOrReadOnly, AuthorAdminOrReadOnly
from .serializers import (IngredientSerializer,
                          RecipeSerializer, TagSerializer)

User = get_user_model()


class TagViewSet(ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (AdminOrReadOnly,)
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('name',)
    lookup_field = 'id'
    pagination_class = None


class IngredientViewSet(ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (AdminOrReadOnly,)
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = IngredientSearchFilter
    search_fields = ('name',)
    pagination_class = None


class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all().order_by('id')
    serializer_class = RecipeSerializer
    permission_classes = (AuthorAdminOrReadOnly,)
    pagination_class = PageNumberPagination
    add_serializer = GetRecipeSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def get_queryset(self):
        carts = Recipe.objects.filter(
            user=OuterRef('pk'),
        )
        favorites = Recipe.objects.filter(
            user=OuterRef('pk'),
        )
        return self.queryset.annotate(
            favorite=Exists(favorites)).annotate(
                cart=Exists(carts))

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
        methods=["POST"],
        detail=True,
        permission_classes=[IsAuthenticated]
    )
    def favorite(self, request, pk):
        return self.post_method(
            request=request, pk=pk, serializers=RecipeSerializer)

    @favorite.mapping.delete
    def delete_favorite(self, request, pk):
        return self.delete_method(
            request=request, pk=pk, model=Favorite)

    @action(
        methods=["POST"],
        detail=True,
        permission_classes=[IsAuthenticated])
    def shopping_cart(self, request, pk):
        return self.post_method(
            request=request, pk=pk, serializers=RecipeSerializer)

    @shopping_cart.mapping.delete
    def delete_shopping_cart(self, request, pk):
        return self.delete_method(
            request=request, pk=pk, model=ShoppingCart)

    @action(
        methods=['GET'],
        detail=False,
        permission_classes=(IsAuthenticated,)
    )
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
