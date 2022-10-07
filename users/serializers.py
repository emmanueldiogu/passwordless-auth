from dataclasses import field
from rest_framework import serializers

from users.models import User
from .register import register_user_sample, generate_username
from .validators import CheckOTP

class RegisterUserByEmailSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['email','username']
        read_only_fields = ['username']
    
    def validate(self, attrs):
        email = attrs.get('email', '')
        username = generate_username(attrs.get('email'))
        attrs['username'] = username
        print(attrs)
        return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
    
class VerifyEmailSerializer(serializers.Serializer):
    auth_totp = serializers.IntegerField()
    

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