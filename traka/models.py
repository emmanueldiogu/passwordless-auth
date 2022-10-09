from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.

class Profile(models):
    user = models.OneToOneField(get_user_model, on_delete=models.CASCADE, related_name='user_profile')