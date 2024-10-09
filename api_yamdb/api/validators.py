import re

from django.core.exceptions import ValidationError

from reviews.constants import USER_NAME_REGEX


def username_validator(value):
    unmatched = re.sub(USER_NAME_REGEX, "", value)
    if value == "me":
        raise ValidationError('Имя пользователя "me" использовать нельзя!')
    elif value in unmatched:
        raise ValidationError(
            f"Имя пользователя не должно содержать {unmatched}"
        )
    return value
