from uuid import uuid4

from django.core.mail import send_mail

from api_yamdb.settings import EMAIL_SENDER
from reviews.models import User


def get_user_and_send_mail(username):
    user = User.objects.get(username=username)
    user.confirmation_code = str(uuid4()).split('-')[0]
    user.save()
    send_mail(
        subject='Код подтверждения',
        message=f'Ваш код: {user.confirmation_code}',
        from_email=EMAIL_SENDER,
        recipient_list=[user.email]
    )
