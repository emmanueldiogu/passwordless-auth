from rest_framework import serializers

from .models import Profile

class ProfileSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Profile
        fields = ['id', 'user_id', 'first_name', 'last_name', 'country', 'language', 'gender', 'height', 'height_unit', 'weight', 'weight_unit',]

