from dataclasses import field
from rest_framework import serializers

from users.models import User
from users.selectors.base import fetch_all_users, fetch_user
from .register import register_user_sample, generate_username
from .validators import CheckOTP

class RegisterUserByEmailSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['email','username']
        read_only_fields = ['username']
    
    def validate(self, attrs):
        email = attrs.get('email', '')
        username = generate_username(email=email)
        attrs['username'] = username
        return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
    
class VerifyEmailSerializer(serializers.Serializer):
    otp = serializers.IntegerField()
    email = serializers.EmailField()

    def validate_email(self,value):
        user = fetch_user(email = value)
        if not bool(user):
            raise serializers.ValidationError('email does not exist')
        return user
    

class LoginSerializer(serializers.ModelSerializer):
    
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