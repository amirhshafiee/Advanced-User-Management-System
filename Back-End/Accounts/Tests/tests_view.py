from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from Accounts.models import CustomUser, EmailOTP
from django.core.mail import outbox
import random

class AccountsTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_data = {
            "email": "test@example.com",
            "name": "testuser",
            "password": "Test@1234",
            "phone_number": "09123456789",
        }
        self.user = CustomUser.objects.create_user(**self.user_data)
        self.otp = random.randint(100000, 999999)
        EmailOTP.objects.create(email=self.user.email, otp=self.otp)
        self.login_url = reverse("user-page:login-page")
        self.register_url = reverse("user-page:register-page")
        self.verify_register_url = reverse("user-page:verify-otp-page")
        self.profile_url = reverse("user-page:profile-page")

    def test_register_user(self):
        user_data = {
            "email": "test@example.com",
            "name": "testuser",
            "password": "Test@1234",
            "confirm_password": "Test@1234",
            "phone_number": "09123456789",
        }
        response = self.client.post(self.register_url, user_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("Message", response.data)
        self.assertEqual(len(outbox), 1)  # Check email was sent

    def test_verify_register_otp(self):
        data = {"email": self.user.email, "otp": self.otp}
        response = self.client.post(self.verify_register_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("Access Token", response.data)
        self.assertIn("Refresh Token", response.data)

    def test_login_valid_user(self):
        data = {"username": self.user.email, "password": self.user_data["password"]}
        response = self.client.post(self.login_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("Access Token", response.data)
        self.assertIn("Refresh Token", response.data)

    def test_login_invalid_password(self):
        data = {"username": self.user.email, "password": "WrongPass123"}
        response = self.client.post(self.login_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Error", response.data)

    def test_get_profile_authenticated(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], self.user.email)

    def test_get_profile_unauthenticated(self):
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)