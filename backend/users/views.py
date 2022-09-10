from djoser.views import UserViewSet as DjoserUserViewSet
from rest_framework.status import HTTP_401_UNAUTHORIZED
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from api.mixins import AddDelViewMixin
from .serializers import UserSubscriptionSerializer


class UserViewSet(DjoserUserViewSet, AddDelViewMixin):
    pagination_class = PageNumberPagination
    serializer_class = UserSubscriptionSerializer

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
        serializer = UserSubscriptionSerializer(
            pages, many=True, context={'request': request}
        )
        return self.get_paginated_response(serializer.data)
