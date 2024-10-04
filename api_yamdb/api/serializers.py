from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

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


class TitleGetSerializer(serializers.ModelSerializer):
    """Сериализатор объекта произведений только для GET-запросов."""

    genre = GenreSerializer(many=True, required=True)
    category = CategorySerializer(required=True)

    class Meta:
        fields = ('id', 'name', 'genre', 'category',
                  'description', 'rating', 'year',)
        model = Title


class TitleSerializer(serializers.ModelSerializer):
    """Сериализатор объекта произведений."""

    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True
    )
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )

    class Meta:
        fields = ('id', 'name', 'genre', 'category',
                  'description', 'rating', 'year',)
        read_only_fields = ('rating',)
        model = Title

    def to_representation(self, value):
        return TitleGetSerializer(value).data


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


class AdminSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Follow с правами admin."""
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


class UserSerializer(AdminSerializer):
    """Сериализатор для модели User."""

    def validate_role(self, value):
        if self.instance and value != self.instance.role:
            raise serializers.ValidationError('Роль не подлежит изменению.')
        return value


class SignupSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    username = serializers.RegexField(
        r'^[\w.@+-]+\Z',
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    class Meta:
        model = User
        fields = 'username', 'email'

    def validate_username(self, value):
        if value == 'me' or len(value) > 150:
            raise serializers.ValidationError(
                'Недопустимый username.'
            )
        return value

    def validate_email(self, value):
        if len(value) > 254:
            raise serializers.ValidationError(
                'Максимальная длина 254 символа.'
            )
        return value
