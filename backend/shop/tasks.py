from django.core.mail import send_mail
from celery import shared_task
#from django.core.mail import EmailMessage
import os
from dotenv import load_dotenv

load_dotenv()


@shared_task
def send_email_customer(user):
    """Send an email to the customer"""

    send_mail(
        "Вы зарегистрировались",
        f"Аккаунт был зарегистрирован на вашу почту: {user['email']}\nВаш логин: {user['username']}\nВаш пароль: {user['password1']} ",
        os.getenv("EMAIL_HOST_USER"),
        [user['email']],
        fail_silently=False,
    )
