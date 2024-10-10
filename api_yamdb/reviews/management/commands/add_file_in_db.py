import csv
import os
import sys

import django
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from reviews.models import (Comment, Category, Title, Review,
                            Genre,)
from reviews.constants import FILES, PATH_TO_DATA


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api_yamdb.settings')
django.setup()

User = get_user_model()


def object_create(data, model, related_model: dict = None):
    if related_model:
        field = list(related_model.keys())[0]
        RelatedModel = related_model[field]
        data[field] = RelatedModel.objects.get(
            pk=data[field]
        )
    obj = model(**data)
    obj.save()


def parse_file_and_create_models(file, model, related_model=None):
    path = os.path.abspath(fr'{PATH_TO_DATA}{file}')
    with open(file=path, mode='r', encoding='utf-8',) as f:
        reader = csv.DictReader(f)
        for data in reader:
            try:
                object_create(data, model, related_model)
            except Exception as e:
                raise Exception(f'Возникла ошибка типа {e}')
        sys.stdout.write(f'{file} done!\n')


class Command(BaseCommand):
    help = 'Добавляет данные из .csv файлов в базу данных'

    def handle(self, *args, **options):
        parse_file_and_create_models(FILES['users'], model=User)
        parse_file_and_create_models(FILES['category'], model=Category)
        parse_file_and_create_models(FILES['genre'], model=Genre)
        parse_file_and_create_models(FILES['titles'], model=Title,
                                     related_model={'category': Category})
        parse_file_and_create_models(FILES['genre_title'],
                                     model=Title.genre.through)
        parse_file_and_create_models(FILES['review'], model=Review,
                                     related_model={'author': User})
        parse_file_and_create_models(FILES['comments'], model=Comment,
                                     related_model={'author': User})
