
from django.urls import path
from .views import LoginView, RegisterView, VerifyEmailView

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('verify/email/', VerifyEmailView.as_view()),
]
