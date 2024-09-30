from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Categories(models.Model):
    name = models.CharField(
        max_length=256,
        help_text='Наименование категории',
        verbose_name='категория',
        db_index=True
    )
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name = 'Категории'
        unique_together = ('name', 'slug')

    def __str__(self):
        return self.name


class Genres(models.Model):
    name = models.CharField(
        max_length=256,
        help_text='Наименование жанра',
        verbose_name='жанр',
        db_index=True
    )
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = 'Жанр'
        verbose_name = 'Жанры'
        unique_together = ('name', 'slug')

    def __str__(self):
        return self.name


class Titles(models.Model):
    name = models.CharField(
        max_length=256,
        help_text='Наименование произведения',
        verbose_name='произведение',
        db_index=True
    )
    year = models.IntegerField(verbose_name='год выпуска')
    description = models.TextField(verbose_name='описание')
    rating = models.IntegerField(
        blank=True,
        null=True,
        help_text='Рейтинг на основе оценок пользователей',
        verbose_name='рейтинг',
    )
    genre = models.ManyToManyField(
        Genres,
        db_table='title_genre_link',
        verbose_name='жанр произведения',
    )
    category = models.ForeignKey(
        Categories,
        on_delete=models.CASCADE,
        related_name='genres',
        to_field='slug',
        verbose_name='категория произведения'
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name = 'Произведения'

    def __str__(self):
        return self.name


class Reviews(models.Model):
    text = models.TextField(verbose_name='текст отзыва')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='автор отзыва'
    )
    score = models.IntegerField(
        validators=[
            models.MinValueValidator(1),
            models.MaxValueValidator(10)
        ]
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации',
        db_index=True
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name = 'Отзывы'


class Comments(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='автор комментария'
    )
    review = models.ForeignKey(
        Reviews,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    text = models.TextField(erbose_name='текст комментария')
    pub_date = models.DateTimeField(
        'Дата добавления',
        auto_now_add=True,
        db_index=True)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name = 'Комментарии'
