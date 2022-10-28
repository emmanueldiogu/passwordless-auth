from django.db import models

# Create your models here.
class Profile(models.Model):
    email = models.EmailField(max_length=254, unique=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    registry_ip = models.GenericIPAddressField(blank=True, null=True)
    user_agent_info = models.CharField(max_length=254, blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['date_created']
        
    def __str__(self):
        return self.email
