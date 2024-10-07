from uuid import uuid4

from django.core.mail import send_mail

from api_yamdb.settings import EMAIL_SENDER
from reviews.models import User


def get_user_and_send_mail(username):
    user = User.objects.select_for_update().filter(username=username)
    user.update(confirmation_code=str(uuid4()).split('-')[0])
    send_mail(
        subject='Код подтверждения',
        message=f'Ваш код: {user[0].confirmation_code}',
        from_email=EMAIL_SENDER,
        recipient_list=[user[0].email]
    )
