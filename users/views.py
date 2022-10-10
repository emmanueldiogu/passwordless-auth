from django.contrib.auth import authenticate
from rest_framework import generics, status, views, permissions
from rest_framework.exceptions import AuthenticationFailed

from rest_framework.views import APIView
from rest_framework.response import Response
from .models import User
from .register import generate_username
from .serializers import RegisterUserByEmailSerializer, VerifyEmailSerializer
from .utils import MailerClass, CreateOTP


# Create your views here.

class RegisterView(generics.GenericAPIView):
    
    serializer_class = RegisterUserByEmailSerializer
    
    def post(self, request):
        """
        response = RegisterService.register_user(user,serializer)
        pyotp.TOTP.verify(784733)
        """
        
        try:
            user = request.data
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            email = user['email']
            totp = CreateOTP.generate_totp(email)
            email_body = "Use this otp " + totp.now() + " to verify your account."
            data = {'email_subject':'Verify your email', 'email_body':email_body, 'email_to':user['email']}
            MailerClass.send_email(data)
            
            # user['otp'] = OTP.now
            print(f'Your OTP is: {totp.now()}')
            
        except TypeError as e:
            return Response(data=e, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

class VerifyEmailView(APIView):
    
    @staticmethod
    def post(request):
        try:
            inputs_ = request.data
            validator = VerifyEmailSerializer(data=inputs_)
            validator.is_valid(raise_exception=True)
            user = validator.validated_data.get('email')
            otp = validator.validated_data.get('otp')
            totp = CreateOTP.generate_totp(user.email)
            if user.auth_provider == 'email':
                if totp.verify(otp):
                    user.is_verified = True
                    user.save()
                    registered_user = authenticate(email=user.email)
                    data = {
                        'username': registered_user.username,
                        'email': registered_user.email,
                        'tokens': registered_user.jwt_tokens
                    }
                else:
                    raise AuthenticationFailed(detail="Invalid user login details or expired otp")
                    return Response(data={"details": "Invalid or expired otp"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                raise AuthenticationFailed(detail="Please continue your login using " + user.auth_provider)
        except TypeError as e:
            return Response(data=e, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(data=data, status=status.HTTP_200_OK)

class LoginView(APIView):
    pass
