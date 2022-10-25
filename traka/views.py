from django.shortcuts import render
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet

from .models import Profile
from .serializers import ProfileSerializer


# Create your views here.

class ProfileViewSet(ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    # permission_classes = [AllowAny]

    @action(detail=False, methods=['GET', 'PUT'])
    def me(self, request):
        print(f'User Id info: {request.user.id}')
        profile = Profile.objects.get(
            user_id=request.user.id)
        if request.method == 'GET':
            serializer = ProfileSerializer(profile)
            return Response(serializer.data)
        elif request.method == 'PUT':
            serializer = ProfileSerializer(profile, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
