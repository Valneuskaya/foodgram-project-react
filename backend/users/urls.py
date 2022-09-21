from django.urls import include, path

from rest_framework.routers import DefaultRouter

from .views import UserViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'users/(?P<id>\d+)/',
                UserViewSet)
router.register(r'users/subscriptions/',
                UserViewSet, basename='subscriptions')
router.register(r'users/(?P<id>\d+)/subscribe/',
                UserViewSet)
router.register(r'users/set_password/',
                UserViewSet)


urlpatterns = [
    path("auth/", include("djoser.urls.authtoken")),
    ]
