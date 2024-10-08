from django.contrib.auth import get_user_model
from rest_framework import serializers

from api.utils import get_user_and_send_mail
from reviews.constants import NON_VALID_USERNAME
from reviews.models import Category, Comment, Genre, Review, Title


User = get_user_model()


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор объекта категорий."""

    class Meta:
        fields = ('name', 'slug')
        lookup_field = 'slug'
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор объекта жанров."""

    class Meta:
        fields = ('name', 'slug')
        lookup_field = 'slug'
        model = Genre


class TitleGetSerializer(serializers.ModelSerializer):
    """Сериализатор объекта произведений только для GET-запросов."""

    genre = GenreSerializer(many=True, required=True)
    category = CategorySerializer(required=True)
    rating = serializers.IntegerField(read_only=True, default=None)

    class Meta:
        fields = '__all__'
        model = Title


class TitleSerializer(serializers.ModelSerializer):
    """Сериализатор объекта произведений."""

    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True,
        allow_empty=False
    )
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )

    class Meta:
        fields = '__all__'
        model = Title

    def to_representation(self, value):
        return TitleGetSerializer(value).data


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор объекта отзывов."""

    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        fields = ('id', 'author', 'text', 'score', 'pub_date')
        read_only_fields = ('id', )
        model = Review

    def create(self, validated_data):
        """Запрещает повторный отзыв тем же пользователем."""

        user = self.context['request'].user
        title_id = (self.context
                    .get('request')
                    .parser_context.get('kwargs')
                    .get('title_id'))
        if Review.objects.filter(
            author=user,
            title=title_id
        ).exists():
            raise serializers.ValidationError(
                'Отзыв уже оставлен'
            )
        return super().create(validated_data)


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор объектов комментариев."""

    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        fields = ('id', 'author', 'text', 'pub_date')
        read_only_fields = ('id', )
        model = Comment


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для модели User."""

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name',
                  'email', 'bio', 'role')

    def validate(self, data):
        """Запрещает пользователям присваивать себе имя me
        и использовать повторные username и email."""
        if data.get('username') == NON_VALID_USERNAME:
            raise serializers.ValidationError(
                'Использовать имя me запрещено'
            )
        if User.objects.filter(username=data.get('username')):
            raise serializers.ValidationError(
                'Пользователь с таким username уже существует'
            )
        if User.objects.filter(email=data.get('email')):
            raise serializers.ValidationError(
                'Пользователь с таким email уже существует'
            )
        return data


class SignupSerializer(serializers.ModelSerializer):
    """Сериализатор для метода регистрации."""

    class Meta:
        model = User
        fields = ('username', 'email')

    def create(self, validated_data):
        user, created = User.objects.get_or_create(
            username=validated_data['username'],
            email=validated_data['email']
        )
        return user

    def validate_username(self, value):
        if value == NON_VALID_USERNAME:
            raise serializers.ValidationError(
                'Недопустимый username.'
            )
        return value


class TokenSerializer(serializers.Serializer):
    """Сериализатор для запроса токена."""

    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)
