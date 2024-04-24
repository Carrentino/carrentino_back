from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string


@shared_task
def send_password_change_email(email, code, first_name, last_name):
    message = render_to_string('password_change_email.html', {
                               'code': code, 'first_name': first_name, 'last_name': last_name})
    send_mail(
        'Смена пароля',
        f'Код для смены пароля: {code}',
        settings.DEFAULT_FROM_EMAIL,
        [email],
        html_message=message,
    )
