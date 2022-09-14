from django.urls import include, path
from rest_framework.routers import DefaultRouter

from users.views import UserViewSet

from .views import IngredientViewSet, RecipeViewSet, TagViewSet

app_name = 'api'

router = DefaultRouter()
router.register('tags', TagViewSet, 'tags')
router.register(r'tags/<int:pk>/', TagViewSet)
router.register('ingredients', IngredientViewSet, 'ingredients')
router.register(r'ingredients/<int:pk>/', IngredientViewSet)
router.register('recipes', RecipeViewSet, 'recipes')
router.register(r'recipes/<int:pk>/', RecipeViewSet)
router.register('recipes/download_shopping_cart/', RecipeViewSet)
router.register(r'recipes/<int:pk>/shopping_cart/', RecipeViewSet)
router.register(r'recipes/<int:pk>/favorite/', RecipeViewSet)
router.register('users', UserViewSet, 'users')


urlpatterns = (
    path('auth/', include('djoser.urls.authtoken')),
    path('', include(router.urls)),
    path('', include('djoser.urls')),
)
