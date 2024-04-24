import smtplib

from django.conf import settings


def send_mail(message: str, to_email: str, title: str):
    smtp_server = "smtp.timeweb.ru"
    port = 465
    server = smtplib.SMTP_SSL(smtp_server, port)
    email = settings.SMTP_EMAIL
    password = settings.SMTP_PASSWORD
    server.login(email, password)
    from_email = email
    server.sendmail(from_email, to_email, message)
    server.quit()
