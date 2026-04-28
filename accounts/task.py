from celery import shared_task
import smtplib
from dotenv import load_dotenv
from twilio.rest import Client
import os
from .models import User
from django.shortcuts import get_object_or_404


load_dotenv('.env')

@shared_task
def send_email_otp(OTP, to_email):
    with smtplib.SMTP('smtp.gmail.com',587) as server:
        server.starttls()
        email = os.getenv('EMAIL')
        server.login(user=email,password=os.getenv('EMAIL_PASSWORD'))

        subject = "Email Verification OTP"
        message = (
            f"Your One-Time Password (OTP) for email verification is {OTP}.\n\n"
            f"This OTP is valid for a limited time. Please do not share it with anyone."
        )

        server.sendmail(
            from_addr=email,
            to_addrs=to_email,
            msg=f"Subject: {subject}\n\n{message}"
        )
        print('success')

@shared_task
def send_sms(OTP, to_no):
    client = Client(os.getenv('TWILIO_SID'),
                    os.getenv('TWILIO_AUTH'))

    message = client.messages.create(
        body=(
            f"Your OTP for verification is {OTP}. "
            f"It is valid for a limited time. Do not share it with anyone."
            ),
        from_=os.getenv('FROM_NO'),
        to=to_no.replace(" ",'')
    )

@shared_task
def delete_user(email, phone_no):
    user = get_object_or_404(User, email=email, phone_no=phone_no)
    if user.user_type == 'candidate' and not user.candidate.is_verified:
        user.delete()
    elif user.user_type == 'company' and not user.company.otp_verified:
        user.delete()