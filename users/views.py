from django.contrib.auth import authenticate
from rest_framework import generics, status, views, permissions
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from traka import serializers
from .models import User
from .serializers import LoginSerializer, RegisterUserByEmailSerializer, VerifyEmailSerializer
from .utils import MailerClass, CreateOTP
from .validators import VerifyEmailValidator
from .services.registration import UserService


# Create your views here.

class TokenObtainPairView(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer

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
        return Response(data={"success":False, "message":serializer.errors['email'][0], "status":status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
        

class VerifyEmailView(generics.GenericAPIView):
    
    permission_classes = [AllowAny,]
    serializer_class = VerifyEmailSerializer
    
    def post(self, request):
        inputs_ = request.data
        validator = self.serializer_class(data=inputs_)
        validator.is_valid(raise_exception=True)
        return Response(data=validator.data, status=status.HTTP_200_OK)
        

class LoginView(generics.GenericAPIView):
    
    permission_classes = [AllowAny,]
    serializer_class = LoginSerializer
    
    def post(self, request):
        inputs_ = request.data
        validator = self.serializer_class(data=inputs_)
        if (validator.is_valid()):
            email = validator.validated_data.get('email')
            data = UserService.register_user(email=email, serializer=validator)
            return Response(data=data, status=status.HTTP_200_OK)
        return Response(data=validator.errors, status=status.HTTP_400_BAD_REQUEST)
