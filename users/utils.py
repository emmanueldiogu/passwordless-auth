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
            from_email='noreply@activepointsplus.com',
            to=[data['email_to']],
        )
        email.send()
        
        
class CreateOTP:
    
    @staticmethod
    def return_key(email_or_mobile):
        """
        Generates a secrete key based by concatinating 
        email or mobile, current datetime and a secret key.
        """
        return str(email_or_mobile) + str(datetime.date(datetime.now())) + 'secretkey'
    
    @classmethod
    def generate_totp(cls, email_or_mobile):
        """
        # converts the generated key into a base32 
        # encoded secrete using base64 
        # the key is passed in with the number of 
        # digits (default=6 digits) to return and the 
        # expiry time (default is 1 minute (60s))
        """
        keygen = cls.return_key(email_or_mobile)
        key = base64.b32encode(keygen.encode())
 
        totp = pyotp.TOTP(key, digits=6, interval = TOTP_EXPIRY_TIME)
        return totp


import inspect
class ReviewerMixin:
    @classmethod
    def run_checks(cls, **kwarg):
        application = cls(**kwarg)
        functions = inspect.getmembers(cls, inspect.isfunction)
        checks = [
            func for func_name, func in functions if func_name.startswith("check")
        ]
        checks.reverse()
        for check in checks:
            application_check = check(application)
            if application_check.get("success") is False:
                return {
                    "success": False,
                    "message": application_check.get("message"),
                    **application_check,
                }
        return {"success": True, "message": "Application checks Successful"}