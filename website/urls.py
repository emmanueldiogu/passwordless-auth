from django.urls import path, include
from rest_framework import routers

from website.views import ProfileViewSet, VerifyEmail

router = routers.DefaultRouter()
router.register('profile', ProfileViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('verify/', VerifyEmail.as_view(), name='verify'),
]
