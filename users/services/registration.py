import base64, pyotp
from datetime import datetime
from django.shortcuts import render

from users.constants import TOTP_EXPIRY_TIME
from ..utils import MailerClass


class UserService:
    @staticmethod
    def return_key(email):
        return str(email) + str(datetime.date(datetime.now())) + 'secretkey'
    
    @classmethod
    def generate_otp(cls, email):
        keygen = cls.return_key(email)
        key = base64.b32encode(keygen.encode())
        totp = pyotp.TOTP(key, digits=6, interval = TOTP_EXPIRY_TIME)
        return totp

    @classmethod
    def register_user(cls,email,serializer):
        email = email
        email_body = "Use this otp " + cls.generate_otp(email=email).now() + " to verify your account."
        data = {'email_subject':'Verify your email', 'email_body':email_body, 'email_to':email}
        MailerClass.send_email(data)
        user = serializer.data
        return {"success":True,"message":"Successfully register user","user":user}