from django.contrib.auth import authenticate
from .models import User
import os
import random
from rest_framework.exceptions import AuthenticationFailed

def generate_username(email):
    username = "".join(email.split('@', 1)[0]).lower()
    if not User.objects.filter(username=username).exists():
        return username
    else:
        random_username = username + str(random.randint(0, 1000))
        return generate_username(random_username)
        

def register_user_sample(provider, user_id, email):
    filtered_user_by_email = User.objects.filter(email=email)
    
    if filtered_user_by_email.exists():
        
        if provider == filtered_user_by_email[0].auth_provider:
            registered_user = authenticate(email=email)
            
            return {
                'usernmae': registered_user.username,
                'email': registered_user.email,
                'tokens': registered_user.tokens()
            }
        else:
            raise AuthenticationFailed(
                detail='Please continue your login using ' + filtered_user_by_email[0].auth_provider
            )
    else:
        user = {
            'username': generate_username(email),
            'email': email,
        }
        user = User.objects.create_user(**user)
        user.is_verified = True
        user.auth_prodider = provider
        user.save()
        
        new_user = authenticate(email=email)
        
        return {
            'email': new_user.email,
            'username': new_user.username,
            'tokens': new_user.tokens()
        }