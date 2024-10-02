from django.shortcuts import get_object_or_404
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

    genre = GenresSerializer(many=True, required=False)
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Categories.objects.all()
    )

    class Meta:
        fields = ('id', 'name', 'genre', 'category',
                  'description', 'rating', 'year',)
        read_only_fields = ('rating',)
        model = Titles

    def create(self, validated_data):
        if 'genre' not in validated_data:
            title = Titles.objects.create(**validated_data)
            return title
        print(validated_data)
        genres = validated_data.pop('genre')
        title = Titles.objects.create(**validated_data)
        for genre in genres:
            current_genre = get_object_or_404(
                Genres,
                **genre
            )
            title.genre.create(genre=current_genre)
        return title



class ReviewsSerializer(serializers.ModelSerializer):
    """Сериализатор объекта отзывов."""
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )
    # title = serializers.StringRelatedField(
    #     required=False,
    #     # read_only=True
    # )
    
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
    review = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        read_only_fields = ('pub_date', 'title', 'review',)
        model = Comments
