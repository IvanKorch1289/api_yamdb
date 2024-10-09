from datetime import datetime
from re import sub

from django.core.exceptions import ValidationError

from reviews.constants import NON_VALID_USERNAME, USER_NAME_REGEX


def validate_max_date_title(value):
    if value > int(datetime.now().year):
        raise ValidationError(
            message='Значение года не может быть больше текущего',
            params={"value": value},
        )


def validate_username(value):
    if value == NON_VALID_USERNAME:
        raise ValidationError(
            message='Нельзя использовать me в качестве username',
            params={"value": value},
        )
    elif value in sub(USER_NAME_REGEX, "", value):
        raise ValidationError(
            message='Можно использовать латинские буквы и символы ., @, +, -.',
            params={"value": value},
        )
