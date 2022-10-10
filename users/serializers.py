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
    

class EmailAuthSerializer(serializers.Serializer):
    
    """ Handle serialization of emailrelated data"""
    
    auth_token = serializers.CharField()
    
    def validate_auth_token(self, auth_token):
        user_data = CheckOTP(auth_token)
        
        try:
            user_id = user_data['id']
            email = user_data['email']
            provider = 'email'
            return register_user_sample(
                provider=provider,
                user_id=user_id,
                email=email,
            )
        except Exception as identifier:
            raise serializers.ValidationError(
                'The token is invalid or expired. Please login again.'
            )