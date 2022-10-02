from string import hexdigits

from rest_framework.serializers import ValidationError

from recipes.models import IngredientAmount


def create_ingredients(ingredients, recipe):
    for ingredient in ingredients:
        IngredientAmount.objects.get_or_create(
            recipe=recipe,
            ingredients_id=ingredient['id'],
            amount=ingredient['amount']
        )


def value_validate(value, klass=None):
    if not str(value).isdecimal():
        raise ValidationError(
            f'{value} must include a number'
        )
    if klass:
        obj = klass.objects.filter(id=value)
        if not obj:
            raise ValidationError(
                f'{value} does not exist.'
            )
        return obj[0]


def is_hex_color(value):
    if len(value) not in (3, 6):
        raise ValidationError(
            f'{value} is wrong length ({len(value)}).'
        )
    if not set(value).issubset(hexdigits):
        raise ValidationError(
            f'{value} is not hexadecimal.'
        )
