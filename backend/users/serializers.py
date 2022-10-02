from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from recipes.models import Recipe

from .models import User


class UserSerializer(ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'password',
        )
        extra_kwargs = {'password': {'write_only': True}}
        read_only_fields = 'is_subscribed',

    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        return (
            user.is_authenticated
            and user.subscribers.filter(
                author=obj,
            ).exists()
        )

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


class GetRecipeSerializer(ModelSerializer):
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'tags', 'cooking_time',
                  'is_favorited', 'is_in_shopping_cart')
        read_only_fields = '__all__',


class UserSubscriptionSerializer(ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()
    recipes = GetRecipeSerializer(many=True)
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count',
        )

    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        return (
            user.is_authenticated
            and user.subscribers.filter(
                author=obj,
            ).exists()
        )

    def get_recipes_count(self, obj):
        return Recipe.objects.filter(author=obj).count()
