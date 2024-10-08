import csv
import os

import django
from django.contrib.auth import get_user_model

from reviews.models import Category

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api_yamdb.settings')
django.setup()

User = get_user_model()
# path = os.path.abspath(r'api_yamdb\static\data\category.csv')
direct = os.path.abspath(r'api_yamdb\static\data')
files = os.listdir(direct)


files.pop(files.index('genre_title.csv'))

for file in files:
    path = os.path.abspath(fr'api_yamdb\static\data\{file}')
    print(file)
    data = []

    with open(file=path, encoding='utf-8', mode='r') as f:
        reader = csv.DictReader(f)
        for line in reader:
            line.pop('id')
            if 'user' in line:
                print(line)
                obj = User(**line)
                data.append(obj)

        obj = Category(**line)
        data.append(obj)
        print(data)
        # User.objects.bulk_create(data, ignore_conflicts=True,)
