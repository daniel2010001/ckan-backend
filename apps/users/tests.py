from datetime import timedelta
from django.test import TestCase
from django.urls import reverse
from apps.users.models import User
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import SlidingToken
import time


class UserAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            name="test_django", email="test_django@example.com", password="test_django"
        )

    def test_api_login(self):
        url = reverse("api/login")
        response = self.client.post(url, self.user_credentials())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["name"], "admin")

    def test_api_logout(self):
        url = reverse("api/logout")
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {"key": "value"})

    def test_api_user(self):
        url = reverse("api/users/me")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {"key": "value"})

    def __temp():
        # Generar un token
        user = User.objects.get(username="admin")
        token = SlidingToken.for_user(user)
        token.set_exp(lifetime=timedelta(seconds=5))

        # Simular una espera para la expiración del token
        time.sleep(6)
        token_expired = SlidingToken(token)
        print(
            token_expired.check_exp()
        )  # Debe ser False, ya que el token debería estar expirado

        # Refrescar el token dentro del tiempo de refresco permitido
        refreshed_token = token_expired.refresh()
        print(refreshed_token)  # Debe ser un nuevo token válido
