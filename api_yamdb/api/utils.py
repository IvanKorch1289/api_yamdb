from uuid import uuid4

from django.core.mail import send_mail


def get_user_and_send_mail(user):
    user.update(confirmation_code=str(uuid4()).split('-')[0])
    send_mail(
        subject='Код подтверждения',
        message=f'Ваш код: {user[0].confirmation_code}',
        from_email='info@api_yamdb.not',
        recipient_list=[user[0].email]
    )
