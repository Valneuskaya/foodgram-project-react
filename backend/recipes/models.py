from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import (CASCADE, CharField, DateTimeField, ForeignKey,
                              ImageField, ManyToManyField, Model,
                              PositiveSmallIntegerField, TextField,
                              UniqueConstraint)

User = get_user_model()


class Tag(Model):
    name = CharField(
        verbose_name='Tag',
        max_length=200,
        unique=True,
    )
    color = CharField(
        verbose_name='HEX code',
        max_length=8,
        blank=True,
        null=True,
        default='FF',
    )
    slug = CharField(
        verbose_name='Tag slug',
        max_length=200,
        unique=True,
    )

    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'
        ordering = ('name', )

    def __str__(self) -> str:
        return f'{self.name} (color: {self.color})'


class Ingredient(Model):
    name = CharField(
        verbose_name='Ingredient',
        max_length=200,
    )
    measurement_unit = CharField(
        verbose_name='Measurement unit',
        max_length=200,
    )

    class Meta:
        verbose_name = 'Ingredient'
        verbose_name_plural = 'Ingredients'
        ordering = ('name', )

    def __str__(self) -> str:
        return f'{self.name} {self.measurement_unit}'


class Recipe(Model):
    name = CharField(
        verbose_name='Recipe name',
        max_length=200,
    )
    author = ForeignKey(
        verbose_name='Recipe author',
        related_name='recipes',
        to=User,
        on_delete=CASCADE,
    )
    ingredients = ManyToManyField(
        verbose_name='Recipe ingredients',
        related_name='recipes',
        to=Ingredient,
        through='recipes.IngredientAmount',
    )
    tags = ManyToManyField(
        verbose_name='Tag',
        related_name='recipes',
        to='Tag',
    )
    image = ImageField(
        verbose_name='Recipe picture',
        upload_to='recipe_images/',
    )
    text = TextField(
        verbose_name='Recipe description',
        max_length=5000,
    )
    cooking_time = PositiveSmallIntegerField(
        verbose_name='Cooking time',
        default=0,
        validators=(
            MinValueValidator(1),
            MaxValueValidator(600),
        ),
    )
    favorite = ManyToManyField(
        verbose_name='Favorite recipes',
        related_name='favorites',
        to=User,
    )
    cart = ManyToManyField(
        verbose_name='Cart list',
        related_name='carts',
        to=User,
    )
    pub_date = DateTimeField(
        verbose_name='Publication date',
        auto_now_add=True,
    )

    class Meta:
        verbose_name = 'Recipe'
        verbose_name_plural = 'Recipes'
        ordering = ('-pub_date', )

    def __str__(self) -> str:
        return f'{self.name}. Author: {self.author.username}'


class IngredientAmount(Model):
    recipe = ForeignKey(
        verbose_name='What recipes',
        related_name='recipes',
        to=Recipe,
        on_delete=CASCADE,
    )
    ingredients = ForeignKey(
        verbose_name='Linked ingredients',
        related_name='ingredients',
        to=Ingredient,
        on_delete=CASCADE,
    )
    amount = PositiveSmallIntegerField(
        verbose_name='Amount',
        default=0,
        validators=(
            MinValueValidator(1),
            MaxValueValidator(10000),
        ),
    )

    class Meta:
        verbose_name = 'Ingredient',
        verbose_name_plural = 'Ingredients',
        ordering = ('recipe', )

    def __str__(self) -> str:
        return f'{self.amount} {self.ingredients}'


class Favorite(Model):
    user = ForeignKey(
        User,
        on_delete=CASCADE,
        verbose_name='User',
    )
    recipe = ForeignKey(
        Recipe,
        on_delete=CASCADE,
        related_name='favorites',
        verbose_name='Recipe',
    )

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Favorite recipe'
        verbose_name_plural = 'Favorite recipes'
        constraints = [
            UniqueConstraint(
                fields=(
                    'user',
                    'recipe',
                ),
                name='unique_favorite_user_recipe',
            )
        ]

    def __str__(self):
        return f'{self.user} added recipe {self.recipe}'


class ShoppingCart(Model):
    user = ForeignKey(
        User,
        on_delete=CASCADE,
        related_name='shoppingcart',
        verbose_name='User',
    )
    recipe = ForeignKey(
        Recipe,
        on_delete=CASCADE,
        related_name='shoppingcart',
        verbose_name='Recipe',
    )

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Cart'
        constraints = [
            UniqueConstraint(
                fields=(
                    'user',
                    'recipe',
                ),
                name='unique_shoppingcart_user_recipe',
            )
        ]

    def __str__(self):
        return f'{self.user} added recipe {self.recipe}'
