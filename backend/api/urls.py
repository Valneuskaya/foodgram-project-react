from django.urls import include, path

from rest_framework.routers import DefaultRouter

from users.views import UserViewSet

from .views import IngredientViewSet, RecipeViewSet, TagViewSet

app_name = 'api'

router = DefaultRouter()
router.register(r'tags', TagViewSet, 'tags')
router.register(r'ingredients', IngredientViewSet, 'ingredients')
router.register(r'recipes', RecipeViewSet, 'recipes')
# router.register(r'recipes/download_shopping_cart', RecipeViewSet)
# router.register(r'recipes/<int:pk>/shopping_cart', RecipeViewSet)
# router.register(r'recipes/<int:pk>/favorite', RecipeViewSet)
router.register(r'users', UserViewSet, 'users')


urlpatterns = (
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
)
