from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.viewsets import generics
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

import jwt

from .models import Profile
from .serializers import ProfileSerializer
from .utils import SendMailClass

# Create your views here.

class ProfileViewSet(ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class =  ProfileSerializer
    
    def get_permissions(self):
        if self.request.method in ['GET', 'PUT', 'PATCH', 'DELETE']:
            return [IsAdminUser()]
        return [AllowAny()]
    
    def create(self, request):
        data = request.data
        serializer = self.serializer_class(data=data)
        if (serializer.is_valid()):
            serializer.save()
            profile = serializer.data
            email_to = profile['email']
            user = Profile.objects.get(email=email_to)
            print(serializer.data)
            print(request)
            token = RefreshToken.for_user(user).access_token
            # token = 'token sent'
            
            current_site = get_current_site(request).domain
            print(get_current_site(request).domain)
            relative_link = reverse('verify')
            absurl = 'http://'+current_site+relative_link+"?token="+str(token)
            email_body = 'Hi, '+email_to+ ' Use this link below to verify your email \n'+'Domain: '+absurl
            data = {'email_body':email_body, 'email_subject': 'Verify your email', 'email_to':email_to}
            
            SendMailClass.send_email(data=data)
            
            # return SendMailClass.send_email(data=data)
            return Response(data=profile, status=status.HTTP_201_CREATED)

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VerifyEmail(generics.GenericAPIView):
    def get(self, request):
        token=request.GET.get('token')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY)
            user = Profile.objects.get(id=payload['user_id'])
            if not user.is_verified:
                user.is_verified = True
                user.save()
            return Response({'success':True, 'message':'Email successfully activated'}, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError as identifier:
            return Response({'success':False,'message':'Activation expired'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as identifier:
            return Response({'success':False,'message':'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
