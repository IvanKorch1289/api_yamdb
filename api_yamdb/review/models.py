from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator

ROLE_CHOICES = (
    ('user', 'Пользователь'), ('moderator', 'Модератор'), ('admin', 'Админ')
)


class MyUser(AbstractUser):
    email = models.EmailField(
        unique=True,
    )
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
        default=email,
        unique=True,
    )
    first_name = models.CharField(
        max_length=150,
    )
    last_name = models.CharField(
        max_length=150,
    )
    bio = models.TextField(blank=True)
    role = models.CharField(
        choices=ROLE_CHOICES,
        default='user',
        max_length=15,
    )
