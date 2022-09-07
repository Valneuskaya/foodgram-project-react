from django.contrib.auth import get_user_model

from recipes.models import Ingredient, Recipe, Tag

from rest_framework.serializers import (ModelSerializer,
                                        SerializerMethodField,
                                        ValidationError)

User = get_user_model()


class GetRecipeSerializer(ModelSerializer):
    class Meta:
        model = Recipe
        fields = 'id', 'name', 'image', 'cooking_time'
        read_only_fields = '__all__',


class UserSerializer(ModelSerializer):
    if_subscribed = SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'first_name',
            'last_name',
            'username',
            'password',
            'is_subscribed',
        )
        kwargs = {'password': {'write_only': True}}
        read_only_fields = 'is_subscribed',

    def get_if_subscribed(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous or (user == obj):
            return False
        return user.subscribe.filter(id=obj.id).exists()

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    def validate_username(self, username):
        if len(username) < 3:
            raise ValidationError(
                'Username length is allowed between '
                f'{3} до {200}'
            )
        if not username.isalpha():
            raise ValidationError(
                'Username allows only letters'
            )
        return username.capitalize()


class UserSubscribeSerializer(UserSerializer):
    recipes = GetRecipeSerializer(many=True, read_only=True)
    recipes_count = SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'first_name',
            'last_name',
            'username',
            'is_subscribed',
            'recipes',
            'recipes_count',
        )
        read_only_fields = '__all__',

    def get_if_subscribed(*args):
        return True

    def get_recipes_count(self, obj):
        return obj.recipes.count()
