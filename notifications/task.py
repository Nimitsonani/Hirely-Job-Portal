from .models import Notification
from celery import shared_task
import smtplib
from dotenv import load_dotenv
import os
from accounts.models import User
from django.shortcuts import get_object_or_404


load_dotenv('.env')


@shared_task
def send_notification(user_email, title, message):
    user = get_object_or_404(User, email=user_email)
    Notification.objects.create(
        user = user,
        title = title,
        message = message
    )
    with smtplib.SMTP('smtp.gmail.com',587) as server:
        server.starttls()
        email = os.getenv('EMAIL')
        server.login(user = email, password=os.getenv('EMAIL_PASSWORD'))
        server.sendmail(
            from_addr=email,
            to_addrs=user_email,
            msg = f"Subject: {title} \n\n {message}"
        )