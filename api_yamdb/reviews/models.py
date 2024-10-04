import random

from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.validators import (MaxValueValidator,
                                    MinValueValidator,
                                    RegexValidator)
from django.db import models


ROLE_CHOICES = (
    ('user', 'Пользователь'),
    ('moderator', 'Модератор'),
    ('admin', 'Админ')
)
SHORT_TITLE = 25


class User(AbstractUser):
    email = models.EmailField(unique=True,)
    username = models.CharField(
        max_length=150,
        validators=[
            RegexValidator(
                regex=r'^[\w.@+-]+\Z',
                message=(
                    'Можно использовать латинские буквы и символы ., @, +, -.'
                ),
                code="invalid_username",
            ),
        ],
        unique=True,
    )
    first_name = models.CharField(max_length=150,)
    last_name = models.CharField(max_length=150,)
    bio = models.TextField(blank=True)
    role = models.CharField(
        choices=ROLE_CHOICES,
        default='user',
        max_length=15,
    )
    confirmation_code = models.CharField(
        max_length=10,
        default=random.randint(1111111111, 9999999999)
    )


class Category(models.Model):
    name = models.CharField(
        max_length=256,
        help_text='Наименование категории',
        verbose_name='категория',
        db_index=True
    )
    slug = models.SlugField(unique=True, primary_key=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name = 'Категории'
        unique_together = ('name', 'slug')

    def __str__(self):
        return self.name[:SHORT_TITLE]


class Genre(models.Model):
    name = models.CharField(
        max_length=256,
        help_text='Наименование жанра',
        verbose_name='жанр',
        db_index=True
    )
    slug = models.SlugField(unique=True, primary_key=True)

    class Meta:
        verbose_name = 'Жанр'
        verbose_name = 'Жанры'
        unique_together = ('name', 'slug')

    def __str__(self):
        return self.name[:SHORT_TITLE]


class Title(models.Model):
    name = models.CharField(
        max_length=256,
        help_text='Наименование произведения',
        verbose_name='произведение',
        db_index=True
    )
    year = models.IntegerField(verbose_name='год выпуска')
    description = models.TextField(verbose_name='описание')
    genre = models.ManyToManyField(
        Genre,
        default=None,
        verbose_name='жанр произведения',
        related_name='titlegenres',
    )
    category = models.ForeignKey(
        Category,
        default=None,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='genries',
        to_field='slug',
        verbose_name='категория произведения'
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name = 'Произведения'

    def __str__(self):
        return self.name[:SHORT_TITLE]


class Review(models.Model):
    text = models.TextField(verbose_name='текст отзыва')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='автор отзыва',
    )
    score = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации',
        db_index=True
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews'
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name = 'Отзывы'
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_title_review_'
            )
        ]

    def __str__(self):
        return self.text[:SHORT_TITLE]


class Comment(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='автор комментария'
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    text = models.TextField(verbose_name='текст комментария')
    pub_date = models.DateTimeField(
        'Дата добавления',
        auto_now_add=True,
        db_index=True)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name = 'Комментарии'

    def __str__(self):
        return self.text[:SHORT_TITLE]
