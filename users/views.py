import base64, pyotp
from datetime import datetime
from django.shortcuts import render
from rest_framework import generics, status, views, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import User
from .register import generate_username
from .serializers import RegisterUserByEmailSerializer, VerifyEmailSerializer
from .utils import Util


# Create your views here.
EXPIRY_TIME = 300

class GenerateKey:
    @staticmethod
    def return_key(email):
        return str(email) + str(datetime.date(datetime.now())) + 'secretkey'

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
            keygen = GenerateKey()
            email = user['email']
            key = base64.b32encode(keygen.return_key(email).encode())
            totp = pyotp.TOTP(key, digits=6, interval = EXPIRY_TIME)
            email_body = "Use this otp " + totp.now() + " to verify your account."
            data = {'email_subject':'Verify your email', 'email_body':email_body, 'email_to':user['email']}
            Util.send_email(data)
            
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
            keygen = GenerateKey()
            user = validator.validated_data.get('email')
            otp = validator.validated_data.get('auth_totp')
            key = base64.b32encode(keygen.return_key(user.email).encode())
            totp = pyotp.TOTP(key, digits=6, interval = EXPIRY_TIME)
            if totp.verify(otp):
                # User.objects.get(email=email)
                user.is_verified = True
                user.save()
            else:
                return Response(data={"details": "Invalid otp"}, status=status.HTTP_400_BAD_REQUEST)
            # user['otp'] = OTP.now
            print(f'Your OTP is: {totp.now()}')
            
        except TypeError as e:
            return Response(data=e, status=status.HTTP_400_BAD_REQUEST)
        
        return Response("User created successfull", status=status.HTTP_200_OK)

class LoginView(APIView):
    pass
