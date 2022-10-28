from django.contrib.auth import authenticate
from django.db.transaction import atomic
from rest_framework.exceptions import AuthenticationFailed

from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer 

from traka.models import Profile

from users.models import User
from users.selectors.base import fetch_all_users, fetch_user
from users.utils import CreateOTP
from users.validators import VerifyEmailValidator
from .register import register_user_sample, generate_username

class RegisterUserByEmailSerializer(serializers.ModelSerializer):
    
    @atomic()
    def save(self, **kwargs):
        user = super().save(**kwargs)
        Profile.objects.create(user=user)

    class Meta:
        model = User
        fields = ['email','username']
        read_only_fields = ['username']
    
    def validate(self, attrs):
        email = attrs.get('email', '')
        username = generate_username(email=email)
        attrs['username'] = username
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({"email": ('Email already exists')})
        return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
    
class VerifyEmailSerializer(serializers.ModelSerializer):
    
    email = serializers.EmailField(max_length=255, min_length=5)
    username = serializers.CharField(max_length=60, read_only=True)
    otp = serializers.IntegerField(write_only=True)
    tokens = serializers.SerializerMethodField()
    
    def get_tokens(self, obj):
        user = User.objects.get(email=obj['email'])
        return {
            'refresh': user.tokens['refresh'],
            'access': user.tokens['access']
        }

    class Meta:
        model = User
        fields = ['email', 'username', 'otp', 'tokens']
    
    def validate(self, attrs):
        email = attrs.get('email', '')
        otp = attrs.get('otp', '')
        totp = CreateOTP.generate_totp(email)
        user = User.objects.get(email=email)
        checks = VerifyEmailValidator.run_checks(**{"otp":otp,"totp":totp,"user":user})
        if not checks.get('success'):
            raise AuthenticationFailed(checks)
        if not user.is_verified:
            user.is_verified = True
            user.save()
        registered_user = authenticate(email=user.email)
        if not registered_user:
            raise AuthenticationFailed("Invalid credentials")
        
        return {
            'email': user.email,
            'username': user.username,
            'tokens': user.tokens
        }
    

class LoginSerializer(serializers.ModelSerializer):
    """
    This is for documentation
    """
    email = serializers.EmailField()
    username = serializers.CharField(read_only=True)
    
    class Meta:
        model = User
        fields = ['email','username']
        read_only_fields = ['username']
    
    def validate_email(self,value):
        user = fetch_user(email = value)
        if not bool(user):
            raise serializers.ValidationError('email does not exist')
        if not user.auth_provider == 'email':
            raise serializers.ValidationError('Login with your '+ user.auth_provider)
        return user