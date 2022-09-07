from datetime import datetime as dt
from urllib.parse import unquote

from django.contrib.auth import get_user_model
from django.db.models import F, Sum
from django.http.response import HttpResponse

from djoser.views import UserViewSet as DjoserUserViewSet

from recipes.models import Ingredient, IngredientAmount, Recipe, Tag

from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from .mixins import AddDelViewMixin
from .permissions import AdminOrReadOnly, AuthorAdminOrReadOnly
from .serializers import (IngredientSerializer, RecipeSerializer,
                          GetRecipeSerializer, TagSerializer,
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
