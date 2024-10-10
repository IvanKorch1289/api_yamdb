import csv
import os

import django
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from reviews.models import (Comment, Category, Title, Review,
                            Genre,)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api_yamdb.settings')
django.setup()

User = get_user_model()


FILES = {
    'users': 'users.csv',
    'category': "category.csv",
    'genre': 'genre.csv',
    'titles': 'titles.csv',
    'genre_title': 'genre_title.csv',
    'review': 'review.csv',
    'comments': 'comments.csv'
}


def user_create(data):
    user = User(**data)
    user.save()


def category_create(data):
    category = Category(**data)
    category.save()


def genre_create(data):
    genre = Genre(**data)
    genre.save()


def title_create(data):
    data['category'] = Category.objects.get(
        pk=data['category']
    )
    title = Title(**data)
    title.save()


def review_create(data):
    data['author'] = User.objects.get(
        pk=data['author']
    )
    review = Review(**data)
    review.save()


def comment_create(data):
    data['author'] = User.objects.get(
        pk=data['author']
    )
    comment = Comment(**data)
    comment.save()


def genre_title_create(data):
    genre_title = Title.genre.through
    genre_title = genre_title(**data)
    genre_title.save()


def parse_file_and_create_models(file, method):
    path = os.path.abspath(fr'api_yamdb\static\data\{file}')
    with open(file=path, mode='r', encoding='utf-8',) as f:
        reader = csv.DictReader(f)
        for data in reader:
            try:
                method(data)
            except Exception as e:
                raise Exception(f'Возникла ошибка типа {e}')
        print(f'{file} done!')


class Command(BaseCommand):
    help = 'Добавляет данные из .csv файлов в базу данных'

    def handle(self, *args, **options):
        parse_file_and_create_models(file=FILES['users'], method=user_create)
        parse_file_and_create_models(FILES['category'], method=category_create)
        parse_file_and_create_models(FILES['genre'], method=genre_create)
        parse_file_and_create_models(FILES['titles'], method=title_create)
        parse_file_and_create_models(FILES['genre_title'],
                                     method=genre_title_create)
        parse_file_and_create_models(FILES['review'], method=review_create)
        parse_file_and_create_models(FILES['comments'], method=comment_create)
