USER = ('user', 'Пользователь')
MODERATOR = ('moderator', 'Модератор')
ADMIN = ('admin', 'Админ')

ROLE_CHOICES = [USER, MODERATOR, ADMIN]

MAX_LEN_ROLE_NAME = max([len(el[0]) for el in ROLE_CHOICES])

DEFAULT_USER_ROLE = USER[0]

SHORT_TITLE = 25

MAX_LENGTH_USERNAME = 150

MAX_FIELD_NAME = 256

MIN_SCORE = 1

MAX_SCORE = 10

USER_NAME_REGEX = r'^[\w.@+-]+\Z'
