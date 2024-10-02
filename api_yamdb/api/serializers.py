from django.contrib.auth import get_user_model

from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from review.models import (Categories, Comments, Genres,
                           Reviews, Titles)


User = get_user_model()


class CategoriesSerializer(serializers.ModelSerializer):
    """Сериализатор объекта категорий."""

    class Meta:
        fields = ('name', 'slug')
        model = Categories


class GenresSerializer(serializers.ModelSerializer):
    """Сериализатор объекта жанров."""

    class Meta:
        fields = ('name', 'slug')
        model = Genres


class TitlesSerializer(serializers.ModelSerializer):
    """Сериализатор объекта произведений."""

    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genres.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Categories.objects.all()
    )

    class Meta:
        fields = ('id', 'name', 'genre', 'category',
                  'description', 'rating', 'year',)
        read_only_fields = ('rating',)
        model = Titles


class ReviewsSerializer(serializers.ModelSerializer):
    """Сериализатор объекта отзывов."""

    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        fields = '__all__'
        read_only_fields = ('pub_date', 'text', 'author',)
        model = Reviews


class CommentsSerializer(serializers.ModelSerializer):
    """Сериализатор объектов комментариев."""

    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        exclude = ('review',)
        read_only_fields = ('pub_date', 'title',)
        model = Comments