from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from django.db.models.query import QuerySet
from django.http import HttpRequest
from django.shortcuts import get_object_or_404
from django.db.models import Avg
from .models import Title, Category, Comment, Genre, Review, User

from .constants import SHORT_TITLE


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    filter_horizontal = ('genre',)
    list_display = (
        'short_name',
        'year',
        'score',
        'category',
        'genres'
    )

    @admin.display(description='Произведение')
    def short_name(self, obj):
        if len(obj.name) <= SHORT_TITLE:
            return f'{obj.name[:SHORT_TITLE]}...'
        return obj.name

    @admin.display(description='Жанры произведения')
    def genres(self, obj):
        genres = get_object_or_404(
            Title,
            pk=obj.pk).genre.all()
        return list(genres)

    def get_queryset(self, request: HttpRequest) -> QuerySet:
        queryset = super().get_queryset(request)
        return queryset.annotate(rating=Avg('reviews__score'))

    @admin.display(description='Рейтинг')
    def score(self, obj):
        return obj.rating


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets
    fieldsets[0][1]['fields'] = fieldsets[0][1]['fields'] + (
        'role', 'bio',
    )
    list_display = ('username', 'email', 'role',)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'short_text',
        'author',
        'score',
        'title',
        'pub_date',
    )

    @admin.display(description='текст отзыва')
    def short_text(self, obj):
        if len(obj.text) <= SHORT_TITLE:
            return f'{obj.text[:SHORT_TITLE]}...'
        return obj.text


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'short_text',
        'author',
        'review',
        'pub_date',
    )

    @admin.display(description='текст отзыва')
    def short_text(self, obj):
        if len(obj.text) <= SHORT_TITLE:
            return f'{obj.text[:SHORT_TITLE]}...'
        return obj.text


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'slug',
    )


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'slug',
    )


admin.site.unregister(Group)
admin.site.empty_value_display = 'Не задано.'
admin.site.site_title = "Администрирование"
admin.site.site_header = "Администрирование"
admin.site.disable_action('delete_selected')
