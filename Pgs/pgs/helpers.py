from django.core.mail import send_mail
import uuid
from django.conf import settings
import os
def send_forget_password_mail(host, email, token):
    
    page_token = f'{host}/set-password/{token}'
    subject = "استعادة كلمة السر"
    masseg = f"قم بالدخول على الرابط لإستعادة كلمة السر {page_token}"
    email_from = os.environ.get('EMAIL_HOST_USER')
    recipient_list = [email]
    send_mail(subject, masseg, email_from, recipient_list)
    return True