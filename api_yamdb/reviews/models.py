from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from reviews.constants import (MAX_FIELD_NAME, MAX_LENGTH_USERNAME, MAX_SCORE,
                               MIN_SCORE, SHORT_TITLE)
from reviews.enums import UserRoles
from reviews.validators import validate_username
from reviews.utils import get_current_year


class NameModel(models.Model):
    """Абстактная модель для общего поля Наименования."""

    name = models.CharField(
        max_length=MAX_FIELD_NAME,
        help_text='Наименование',
        verbose_name='наименование',
        db_index=True
    )

    class Meta:
        abstract = True
        ordering = ['name']

    def __str__(self):
        return self.name[:SHORT_TITLE]


class SlugModel(models.Model):
    """Абстактная модель для общего поля Слаг."""

    slug = models.SlugField(unique=True)

    class Meta:
        abstract = True


class TextAndDateModel(models.Model):
    """Абстактная модель для общего поля Текст и Дата публикации."""

    text = models.TextField(verbose_name='текст отзыва')
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации',
        db_index=True
    )
    author = models.ForeignKey(
        'User',
        on_delete=models.CASCADE,
        verbose_name='автор',
    )

    class Meta:
        abstract = True
        ordering = ['-pub_date']

    def __str__(self):
        return self.text[:SHORT_TITLE]


class User(AbstractUser):
    email = models.EmailField(unique=True,)
    username = models.CharField(
        max_length=MAX_LENGTH_USERNAME,
        validators=[validate_username],
        unique=True,
    )
    bio = models.TextField(blank=True, verbose_name='Биография')
    role = models.CharField(
        verbose_name='роль',
        max_length=UserRoles.max_length_field(),
        choices=UserRoles.choices(),
        default=UserRoles.user.name
    )
    confirmation_code = models.SlugField(
        null=True,
        blank=True
    )

    @property
    def is_admin(self):
        return self.role == UserRoles.admin.name or self.is_superuser

    @property
    def is_moderator(self):
        return self.role == UserRoles.moderator.name


class Category(NameModel, SlugModel):

    class Meta(NameModel.Meta):
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Genre(NameModel, SlugModel):

    class Meta(NameModel.Meta):
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Title(NameModel):

    year = models.IntegerField(
        verbose_name='год выпуска',
        validators=[
            MaxValueValidator(
                get_current_year,
                message='Значение не может превышать текущий год'
            )
        ],
    )
    description = models.TextField(verbose_name='описание')
    genre = models.ManyToManyField(
        Genre,
        default=None,
        verbose_name='жанр произведения',
    )
    category = models.ForeignKey(
        Category,
        default=None,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='категория произведения'
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        default_related_name = 'titles'
        ordering = ['-year', 'name']

    def __str__(self):
        return self.name[:SHORT_TITLE]


class Review(TextAndDateModel):

    score = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(MIN_SCORE),
            MaxValueValidator(MAX_SCORE)
        ],
        verbose_name='Рейтинг',
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='Произведение'
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        default_related_name = 'reviews'
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_title_review_'
            )
        ]


class Comment(TextAndDateModel):

    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        verbose_name='Отзыв'
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        default_related_name = 'comments'
