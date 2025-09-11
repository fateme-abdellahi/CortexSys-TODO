import pytest
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse


# setup api client
@pytest.fixture
def api_client():
    return APIClient()


# authentication
@pytest.fixture
def authenticated_client(api_client):
    user = {
        "username": "test",
        "password": "11111111",
        "password2": "11111111",
        "email": "test@email.com",
    }
    response = api_client.post(reverse("register"), user, format="json")
    assert response.status_code == status.HTTP_201_CREATED
    access_token = response.data["tokens"]["access"]
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")
    return api_client


@pytest.fixture
def list_create_url():
    return reverse("list_create_tasks")


# parametrized test for creating invalid tasks
@pytest.mark.parametrize(
    "invalid_task_creation_data_parametrize",
    [
        # task with missing title
        ({"description": "desc", "status": "pending", "priority": "medium"}),
        # task with invalid status
        ({"title": "test", "status": "not_a_status"}),
        # task with invalid priority
        ({"title": "test", "priority": "urgent"}),
        # task with invalid due_date format
        ({"title": "test", "duo_date": "not-a-date"}),
        # task with empty payload
        ({}),
        # task with very long title
        ({"title": "t" * 300}),
        # task with duplicate title
        ({"title": "unique-title_to_be_duplicated"}),
    ],
)


# test task creation invalid info
@pytest.mark.django_db
def test_create_invalid_todo(
    list_create_url, authenticated_client, invalid_task_creation_data_parametrize
):
    response = authenticated_client.post(
        list_create_url,
        invalid_task_creation_data_parametrize,
        format="json",
    )

    # for duplicate title test
    if (
        invalid_task_creation_data_parametrize.get("title")
        == "unique-title_to_be_duplicated"
    ):
        # create the second task with this title
        response = authenticated_client.post(
            list_create_url,
            invalid_task_creation_data_parametrize,
            format="json",
        )

    # check response status code
    assert response.status_code == status.HTTP_400_BAD_REQUEST


# test task creation successfull
@pytest.mark.django_db
def test_task_creation_successfull(list_create_url, authenticated_client):
    response = authenticated_client.post(
        list_create_url,
        {
            "title": "test",
            "description": "desc",
            "status": "pending",
            "priority": "medium",
        },
        format="json",
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["title"] == "test"
    assert response.data["description"] == "desc"
    assert response.data["status"] == "pending"
    assert response.data["priority"] == "medium"


# payload for update tests as old task info
@pytest.fixture
def old_task_info():
    return {
        "title": "test task",
        "description": "test description",
        "status": "pending",
        "priority": "medium",
        "duo_date": "2025-01-01",
    }


# create the old task info for update tests
@pytest.fixture
def create_task(list_create_url, authenticated_client, old_task_info):
    response = authenticated_client.post(
        list_create_url,
        data=old_task_info,
        content_type="application/json",
    )
    return response.data.get("id")


# get url for update and delete endpoints
@pytest.fixture
def update_delete_url(create_task):
    return reverse("update_delete_tasks", args=[create_task])


@pytest.mark.parametrize(
    "invalid_task_update_data_parametrize",
    [
        # task update with invalid status
        ({"status": "not_a_status"}),
        # task update with invalid priority
        ({"priority": "urgent"}),
        # task update with invalid due_date format
        ({"duo_date": "not-a-date"}),
    ],
)
@pytest.mark.django_db
def test_update_todo_invalid_status(
    old_task_info,
    update_delete_url,
    authenticated_client,
    invalid_task_update_data_parametrize,
):
    data = old_task_info.copy()

    # update the old field with new invalid data
    data.update(invalid_task_update_data_parametrize)
    response = authenticated_client.put(
        update_delete_url, data=data, content_type="application/json"
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
# update task successfull
def test_update_todo(update_delete_url, authenticated_client):
    payload = {}
    payload["title"] = "test - updated"
    payload["status"] = "completed"
    payload["duo_date"] = "2025-01-02"
    payload["priority"] = "high"
    payload["description"] = "updated description"
    response = authenticated_client.put(
        update_delete_url, data=payload, content_type="application/json"
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.data.get("title") == "test - updated"
    assert response.data.get("status") == "completed"
    assert response.data.get("duo_date") == "2025-01-02T00:00:00Z"
    assert response.data.get("priority") == "high"
    assert response.data.get("description") == "updated description"


# test partial update task successfull
@pytest.mark.django_db
def test_partial_update_todo(old_task_info, update_delete_url, authenticated_client):
    partial_payload = {"title": "test - partial update", "status": "completed"}
    response = authenticated_client.put(
        update_delete_url, data=partial_payload, content_type="application/json"
    )
    data = old_task_info.copy()
    assert response.status_code == status.HTTP_200_OK
    assert response.data.get("title") == "test - partial update"
    assert response.data.get("status") == "completed"
    assert response.data.get("duo_date") == data["duo_date"] + "T00:00:00Z"
    assert response.data.get("priority") == data["priority"]
    assert response.data.get("description") == data["description"]


# test delete task successfull
@pytest.mark.django_db
def test_delete_todo(update_delete_url, authenticated_client):
    response = authenticated_client.delete(update_delete_url)
    assert response.status_code == status.HTTP_204_NO_CONTENT


# test delete non-existent task
@pytest.mark.django_db
def test_delete_non_existent_todo(authenticated_client):
    non_existent_url = reverse("update_delete_tasks", args=[3])
    response = authenticated_client.delete(non_existent_url)
    assert response.status_code == status.HTTP_404_NOT_FOUND
