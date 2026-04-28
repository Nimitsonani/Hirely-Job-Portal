from celery import shared_task
import smtplib
from dotenv import load_dotenv
import os

load_dotenv('.env')


@shared_task
def send_email(message):
    with smtplib.SMTP('smtp.gmail.com',587) as server:
        server.starttls()
        email = os.getenv('EMAIL')
        server.login(user = email, password=os.getenv('EMAIL_PASSWORD'))
        server.sendmail(
            from_addr=email,
            to_addrs=os.getenv('PERSONEL_EMAIL'),
            msg = f"Subject: Contact Us Form From Hirely. \n\n {message}"
        )