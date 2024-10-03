from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from reviews.models import (Category, Comment, Genre,
                            Review, Title)


User = get_user_model()


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор объекта категорий."""

    class Meta:
        fields = ('name', 'slug')
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор объекта жанров."""

    class Meta:
        fields = ('name', 'slug')
        model = Genre


class TitleSerializer(serializers.ModelSerializer):
    """Сериализатор объекта произведений."""

    genre = GenreSerializer(many=True, required=False)
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )

    class Meta:
        fields = ('id', 'name', 'genre', 'category',
                  'description', 'rating', 'year',)
        read_only_fields = ('rating',)
        model = Title

    def create(self, validated_data):
        if 'genre' not in validated_data:
            title = Title.objects.create(**validated_data)
            return title
        print(validated_data)
        genres = validated_data.pop('genre')
        title = Title.objects.create(**validated_data)
        for genre in genres:
            current_genre = get_object_or_404(
                Genre,
                **genre
            )
            title.genre.create(genre=current_genre)
        return title



class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор объекта отзывов."""
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )
    title = serializers.StringRelatedField(
        required=False,
        read_only=True
    )

    class Meta:
        fields = '__all__'
        read_only_fields = ('pub_date', 'author',)
        model = Review


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор объектов комментариев."""

    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )
    review = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        fields = '__all__'
        read_only_fields = ('pub_date', 'title',)
        model = Comment


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для модели User."""
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = 'username', 'email', 'first_name', 'last_name', 'bio', 'role'

    def validate_last_name(self, value):
        if len(value) > 150:
            raise serializers.ValidationError(
                'Максимальная длина 150 символов.'
            )
        return value

    def validate_first_name(self, value):
        if len(value) > 150:
            raise serializers.ValidationError(
                'Максимальная длина 150 символов.'
            )
        return value

    def validate_role(self, value):
        if self.instance and value != self.instance.role:
            raise serializers.ValidationError('Роль не подлежит изменению.')
        return value


class AdminSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Follow с правами admin."""
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)


    class Meta:
        model = User
        fields = 'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        