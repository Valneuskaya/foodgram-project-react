from djoser.views import UserViewSet as DjoserUserViewSet

from django.db.models import OuterRef

from rest_framework.status import (
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
)
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Subscription, User
from .serializers import UserSerializer, UserSubscriptionSerializer


class UserViewSet(DjoserUserViewSet):
    queryset = User.objects.all().order_by('id')
    pagination_class = PageNumberPagination
    serializer_class = UserSerializer

    @action(
        detail=True,
        methods=['POST', 'DELETE'],
        url_path='subscribe',
        permission_classes=[IsAuthenticated],
    )
    def subscribe(self, request):
        if request.method == 'POST':
            user = request.user
            author = self.get_object()
            if user == author:
                data = {'errors': 'You cannot subscribe to yourself.'}
                return Response(data, status=HTTP_400_BAD_REQUEST)
            if Subscription.objects.filter(
                user=user,
                author=author,
            ).exists():
                data = {'errors': 'You have already subscribed to the author.'}
                return Response(data, status=HTTP_400_BAD_REQUEST)
            Subscription.objects.create(
                user=user,
                author=author,
            )
            serializer = UserSubscriptionSerializer(
                author,
                context={'request': request},
            )
            return Response(serializer.data, status=HTTP_201_CREATED)
        if request.method == 'DELETE':
            user = request.user
            author = self.get_object()
            subscription = Subscription.objects.filter(
                user=user,
                author=author,
            )
            if subscription.exists():
                subscription.delete()
                return Response(status=HTTP_204_NO_CONTENT)
            data = {'errors': 'You have not been subscribed to the author.'}
            return Response(data, status=HTTP_400_BAD_REQUEST)

    @action(
        detail=False,
        methods=['GET'],
        url_path='subscriptions',
        permission_classes=[IsAuthenticated],
    )
    def subscriptions(self, request):
        user = self.request.user
        if user.is_anonymous:
            return Response(status=HTTP_401_UNAUTHORIZED)
        subscribed_to_authors = Subscription.objects.filter(
            user=user, author=OuterRef('id')
        )
        subscriptions = User.objects.all().filter(
            id__in=(subscribed_to_authors.values('author_id'))
        )
        pages = self.paginate_queryset(subscriptions)
        serializer = UserSubscriptionSerializer(
            pages, many=True, context={'request': request}
        )
        return self.get_paginated_response(serializer.data)
