from datetime import datetime

from django.core.exceptions import ValidationError


def validate_max_date_title(value):
    if value > int(datetime.now().year):
        raise ValidationError(
            message='Значение года не может быть больше текущего',
            params={"value": value},
        )
