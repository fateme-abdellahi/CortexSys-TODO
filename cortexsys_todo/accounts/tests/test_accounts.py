import pytest
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from accounts.models import CustomUser


# add client api
@pytest.fixture
def api_client():
    return APIClient()


# test registeration with correct data
@pytest.mark.django_db
def test_successfull_register(api_client):
    response = api_client.post(
        reverse("register"),
        {
            "username": "test",
            "password": "11111111",
            "password2": "11111111",
            "email": "test@email.com",
        },
        format="json",
    )
    assert response.status_code == status.HTTP_201_CREATED

    CustomUser.objects.get(username="test")


# test password less than 8 characters
@pytest.mark.django_db
def test_short_password(api_client):
    response = api_client.post(
        reverse("register"),
        {
            "username": "test",
            "password": "1",
            "password2": "1",
            "email": "test@email.com",
        },
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST


# test password and password2 not matching
@pytest.mark.django_db
def test_unmatched_passwords(api_client):
    response = api_client.post(
        reverse("register"),
        {
            "username": "test",
            "password": "11111111",
            "password2": "22222222",
            "email": "test@email.com",
        },
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST


# test missing field
@pytest.mark.django_db
def test_missing_field(api_client):
    response = api_client.post(
        reverse("register"),
        {
            "username": "test",
            "password": "11111111",
            "password2": "111111111",
        },
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST


# test existing username
@pytest.mark.django_db
def test_existing_user(api_client):
    api_client.post(
        reverse("register"),
        {
            "username": "test",
            "password": "11111111",
            "password2": "11111111",
            "email": "test@email.com",
        },
    )

    response = api_client.post(
        reverse("register"),
        {
            "username": "test",
            "password": "22222222",
            "password2": "22222222",
            "email": "test2@email.com",
        },
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST


# test existing email
@pytest.mark.django_db
def test_existing_email(api_client):
    api_client.post(
        reverse("register"),
        {
            "username": "test",
            "password": "11111111",
            "password2": "11111111",
            "email": "test@email.com",
        },
    )

    response = api_client.post(
        reverse("register"),
        {
            "username": "test2",
            "password": "22222222",
            "password2": "22222222",
            "email": "test@email.com",
        },
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
