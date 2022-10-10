import base64
from datetime import datetime
from django.core.mail import EmailMessage
import pyotp

from users.constants import *

class MailerClass(EmailMessage):
    @staticmethod
    def send_email(data):
        email = EmailMessage(
            subject=data['email_subject'],
            body=data['email_body'],
            to=[data['email_to']],
        )
        email.send()
        
        
class CreateOTP:
    
    @staticmethod
    def return_key(email_or_mobile):
        return str(email_or_mobile) + str(datetime.date(datetime.now())) + 'secretkey'
    
    @classmethod
    def generate_totp(cls, email_or_mobile):
        keygen = cls.return_key(email_or_mobile)
        key = base64.b32encode(keygen.encode())
        totp = pyotp.TOTP(key, digits=6, interval = TOTP_EXPIRY_TIME)
        return totp