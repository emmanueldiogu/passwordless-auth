from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient, APITestCase

# Create your tests here.
class RegisterTestCase(APITestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(username="emmanowell", email="emma@example.local",)
        self.client = APIClient()
        self.register_url = reverse('register')
        return super().setUp()