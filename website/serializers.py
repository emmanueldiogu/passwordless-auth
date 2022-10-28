from django.forms import IntegerField
from rest_framework import serializers

from website.models import Profile

class ProfileSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = Profile
        fields = ['id', 'email', 'country', 'city', 'registry_ip',]