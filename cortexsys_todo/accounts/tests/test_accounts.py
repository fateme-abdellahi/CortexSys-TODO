from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
import pytest
from accounts.models import CustomUser

@pytest.mark.django_db
class AuthTest(APITestCase):
        
    def test_successfull_register(self):
        response = self.client.post(reverse('register'), {
            "username": "test",
            "password": "11111111",
            "password2": "11111111",
            "email": "test@email.com"
        }, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        
        CustomUser.objects.get(username="test")
        
    def test_short_password(self):
        response = self.client.post(reverse('register'), {
            "username": "test",
            "password": "1",
            "password2": "1",
            "email":"test@email.com"
        })
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        
    def test_unmatched_passwords(self):
        response = self.client.post(reverse('register'), {
            "username": "test",
            "password": "11111111",
            "password2": "22222222",
            "email":"test@email.com"
        })
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        
    def test_missing_field(self):
        response = self.client.post(reverse('register'), {
            "username": "test",
            "password": "11111111",
            "password2": "111111111",
        })
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        
    def test_existing_user(self):
        self.client.post(reverse('register'), {
            "username": "test",
            "password": "11111111",
            "password2": "11111111",
            "email":"test@email.com"
        })
        
        response = self.client.post(reverse('register'), {
            "username": "test",
            "password": "22222222",
            "password2": "22222222",
            "email":"test2@email.com"
        })
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        
    def test_existing_email(self):
        self.client.post(reverse('register'), {
            "username": "test",
            "password": "11111111",
            "password2": "11111111",
            "email":"test@email.com"
        })
        
        response = self.client.post(reverse('register'), {
            "username": "test2",
            "password": "22222222",
            "password2": "22222222",
            "email":"test@email.com"
        })
        assert response.status_code == status.HTTP_400_BAD_REQUEST
