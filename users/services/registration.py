import base64, pyotp
from datetime import datetime
from django.shortcuts import render
from ..utils import MailerClass


class RegisterService:
    @staticmethod
    def return_key(email):
        return str(email) + str(datetime.date(datetime.now())) + 'secretkey'

    @classmethod
    def register_user(cls,user,serializer):
        EXPIRY_TIME = 300
        email = user['email']
        keygen = cls.return_key(email)
        key = base64.b32encode(keygen.return_key(email).encode())
        totp = pyotp.TOTP(key, digits=6, interval = EXPIRY_TIME)
        email_body = "Use this otp " + totp.now() + " to verify your account."
        data = {'email_subject':'Verify your email', 'email_body':email_body, 'email_to':user['email']}
        MailerClass.send_email(data)
        data = serializer.data
        return {"success":True,"message":"Successfully register user","data":data}