from django.contrib.admin import (ModelAdmin, TabularInline,
                                  register, site)

from .models import (Favorite, Ingredient, IngredientAmount,
                     Recipe, ShoppingCart, Tag)

site.site_header = 'Foodgram administration'


@register(Tag)
class TagAdmin(ModelAdmin):
    list_display = (
        'pk',
        'name',
        'color',
        'slug',
    )
    empty_value_display = '-empty-'


@register(Ingredient)
class IngredientAdmin(ModelAdmin):
    list_display = (
        'pk',
        'name',
        'measurement_unit',
    )
    list_filter = ('name',)
    empty_value_display = '-empty-'


@register(IngredientAmount)
class LinksAdmin(ModelAdmin):
    pass


class IngredientInLine(TabularInline):
    model = IngredientAmount
    extra = 10


@register(Recipe)
class RecipeAdmin(ModelAdmin):
    list_display = (
        'name',
        'author',
        'count_favorites',
    )
    list_filter = (
        'author',
        'name',
        'tags',
    )
    inlines = (IngredientInLine,)
    empty_value_display = '-empty-'

    def count_favorites(self, obj):
        return obj.favorites.count()


@register(Favorite)
class FavoriteAdmin(ModelAdmin):
    list_display = (
        'pk',
        'user',
        'recipe',
    )


@register(ShoppingCart)
class ShoppingCartAdmin(ModelAdmin):
    list_display = (
        'pk',
        'user',
        'recipe',
    )
