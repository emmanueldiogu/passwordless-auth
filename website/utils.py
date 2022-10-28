from django.core.mail import EmailMessage


class SendMailClass(EmailMessage):
    
    @staticmethod
    def send_email(data):
        email = EmailMessage(
            subject=data['email_subject'],
            body=data['email_body'],
            from_email='noreply@activepointsplus.com',
            to=[data['email_to']],
        )
        email.send()