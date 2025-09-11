import pytest
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from accounts.models import CustomUser


# add client api
@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
# add register url
def register_url():
    return reverse("register")


# parametrized test for registeration (for empty db)
@pytest.mark.parametrize(
    "username, password, password2, email, expected_status",
    [
        # test registeration with correct data
        ("test", "11111111", "11111111", "test@email.com", status.HTTP_201_CREATED),
        # test password less than 8 characters
        ("test", "1", "1", "test@email.com", status.HTTP_400_BAD_REQUEST),
        # test password and password2 not matching
        ("test", "11111111", "22222222", "test@email.com", status.HTTP_400_BAD_REQUEST),
        # test missing field
        ("test", "11111111", "11111111", None, status.HTTP_400_BAD_REQUEST),
    ],
)
@pytest.mark.django_db
def test_register_for_empty_db(
    register_url, api_client, username, password, password2, email, expected_status
):
    response = api_client.post(
        register_url,
        {
            "username": username,
            "password": password,
            "password2": password2,
            "email": email,
        },
        format="json",
    )
    assert response.status_code == expected_status

    if expected_status == status.HTTP_201_CREATED:
        CustomUser.objects.get(username="test")


# parametrized test for registeration (for already existed data)
@pytest.mark.parametrize(
    "data, expected_status",
    [
        # test existing username
        ({"username": "test"}, status.HTTP_400_BAD_REQUEST),
        # test existing email
        ({"email": "test@email.com"}, status.HTTP_400_BAD_REQUEST),
    ],
)
@pytest.mark.django_db
def test_existing_data(register_url, api_client, data, expected_status):
    api_client.post(
        register_url,
        {
            "username": data.get("username", "test"),
            "password": data.get("password", "11111111"),
            "password2": data.get("password2", "11111111"),
            "email": data.get("email", "test@email.com"),
        },
    )

    response = api_client.post(
        register_url,
        {
            "username": data.get("username", "test2"),
            "password": data.get("password", "22222222"),
            "password2": data.get("password2", "22222222"),
            "email": data.get("email", "test2@email.com"),
        },
    )
    assert response.status_code == expected_status
