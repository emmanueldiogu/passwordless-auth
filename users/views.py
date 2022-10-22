from django.contrib.auth import authenticate
from rest_framework import generics, status, views, permissions
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from .models import User
from .serializers import LoginSerializer, RegisterUserByEmailSerializer, VerifyEmailSerializer
from .utils import MailerClass, CreateOTP
from .validators import VerifyEmailValidator
from .services.registration import UserService


# Create your views here.

class RegisterView(generics.GenericAPIView):
    
    serializer_class = RegisterUserByEmailSerializer
    permission_classes = [AllowAny,]
    
    def post(self, request):        
        user = request.data
        serializer = self.serializer_class(data=request.data)
        if (serializer.is_valid()):
            serializer.save()
            email = user['email']
            data = UserService.register_user(email=email, serializer=serializer)
            return Response(data=data, status=status.HTTP_201_CREATED)
        return Response(data={"success":False, "message":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        

class VerifyEmailView(generics.GenericAPIView):
    
    permission_classes = [AllowAny,]
    serializer_class = VerifyEmailSerializer
    
    def post(self, request):
        inputs_ = request.data
        validator = self.serializer_class(data=inputs_)
        if (validator.is_valid()):
            user = validator.validated_data.get('email')
            otp = validator.validated_data.get('otp')
            totp = CreateOTP.generate_totp(user.email)
            checks = VerifyEmailValidator.run_checks(**{"otp":otp,"totp":totp,"user":user})
            if not checks.get('success'):
                return Response(checks, status=status.HTTP_401_UNAUTHORIZED)
            if not user.is_verified:
                user.is_verified = True
                user.save()
            registered_user = authenticate(email=user.email)
            data = {
                'success': True,
                'message': "Login successful",
                'username': registered_user.username,
                'email': registered_user.email,
                'tokens': registered_user.jwt_tokens
            }
            return Response(data=data, status=status.HTTP_200_OK)
        return Response(data=validator.errors, status=status.HTTP_400_BAD_REQUEST)
        

class LoginView(generics.GenericAPIView):
    
    permission_classes = [AllowAny,]
    serializer_class = LoginSerializer
    
    def post(self, request):
        inputs_ = request.data
        validator = self.serializer_class(data=inputs_)
        print("start here")
        if (validator.is_valid()):
            print("Continue here")
            email = validator.validated_data.get('email')
            data = UserService.register_user(email=email, serializer=validator)
            print("End here")
            return Response(data=data, status=status.HTTP_200_OK)
        return Response(data=validator.errors, status=status.HTTP_400_BAD_REQUEST)
        try:
            inputs_ = request.data
            validator = self.serializer_class(data=inputs_)
            validator.is_valid(raise_exception=True)
            email = validator.validated_data.get('email')
            totp = CreateOTP.generate_totp(email)
            email_body = "Use this otp " + totp.now() + " to log into your account."
            data = {'email_subject':'Verify your email', 'email_body':email_body, 'email_to':email}
            MailerClass.send_email(data)
        except TypeError as e:
            raise AuthenticationFailed(detail=e)
        
        return Response(data=validator.data, status=status.HTTP_200_OK)
