from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from rest_framework_simplejwt.tokens import RefreshToken

# Create your models here.

class UserManager(BaseUserManager):

    def create_user(self, username, email, password=None):
        if username is None:
            raise TypeError('User should have a username')
        if email is None:
            raise TypeError('Users should have an Email')

        if password is not None:
            user = self.model(username=username, email=self.normalize_email(email))
            user.set_password(password)
            user.save()
        else:
            user = self.model(username=username, email=self.normalize_email(email))
            user.set_unusable_password()
            user.save()

        return user
    
    def create_superuser(self, username, email, password):
        if password is None:
            raise TypeError('User must have password')
        if username is None:
            raise TypeError('username is required')
        email = self.normalize_email(email)
        
        user = self.create_user(username, email, password)
        user.set_password(password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        
        return user

AUTH_PROVIDERS = {'facebook': 'facebook', 'google': 'google', 'email': 'email', 'mobile': 'mobile'}

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=60, unique=True)
    mobile = models.CharField(validators=[], max_length=17, blank=True, null=True)
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    auth_provider = models.CharField(max_length=15, blank=False, null=False, default=AUTH_PROVIDERS.get('email'))
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    objects = UserManager()
    
    def __str__(self) -> str:
        return self.email
    
    @property
    def jwt_tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }
