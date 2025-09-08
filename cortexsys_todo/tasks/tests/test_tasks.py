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
    response=api_client.post(reverse("register"),user,format="json")
    assert response.status_code == status.HTTP_201_CREATED
    access_token = response.data["tokens"]["access"]
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")
    return api_client

@pytest.fixture
def list_create_url():
    return reverse("list_create_tasks")

# test creating tasks
@pytest.mark.django_db
class TestCreateTodo:

# test task creation successfull
    def test_task_creation_successfull(self,list_create_url,authenticated_client):
        response = authenticated_client.post(list_create_url,{"title":"test","description": "desc", "status": "pending", "priority": "medium"},
            format="json")
        
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["title"] == "test"
        assert response.data["description"] == "desc"
        assert response.data["status"] == "pending"
        assert response.data["priority"] == "medium"

# test task creation invalid info

    def test_create_todo_missing_title(self,list_create_url,authenticated_client):
        response = authenticated_client.post(
            list_create_url,
            {"description": "desc", "status": "pending", "priority": "medium"},
            format="json",
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_todo_invalid_status(self,list_create_url,authenticated_client):
            response = authenticated_client.post(
            list_create_url,
            {"title": "test", "status": "not_a_status"},
            content_type="application/json",
        )
            assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_todo_invalid_priority(self,list_create_url,authenticated_client):
        response = authenticated_client.post(
            list_create_url,
            {"title": "test", "priority": "urgent"},
            content_type="application/json",
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_todo_invalid_due_date_format(self,list_create_url,authenticated_client):
        response = authenticated_client.post(
            list_create_url,
            {"title": "test", "duo_date": "not-a-date"},
            content_type="application/json",
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_todo_empty_payload(self,list_create_url,authenticated_client):
        response = authenticated_client.post(list_create_url, {}, content_type="application/json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_todo_long_title(self,list_create_url,authenticated_client):
        long_title = "t" * 300
        response = authenticated_client.post(
            list_create_url, {"title": long_title}, content_type="application/json"
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_todo_duplicate_title(self,list_create_url,authenticated_client):
        authenticated_client.post(
            list_create_url, {"title": "unique-title"}, content_type="application/json"
        )
        response = authenticated_client.post(
            list_create_url, {"title": "unique-title"}, content_type="application/json"
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST


# test updating tasks

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
def create_task(list_create_url,authenticated_client,old_task_info):
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

# update tasks test class
@pytest.mark.django_db
class TestUpdateTodo:

    # update task successfull
    def test_update_todo(self,update_delete_url,authenticated_client):
        payload={}
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

# update task by invalid info

    def test_update_todo_invalid_status(self,old_task_info,update_delete_url,authenticated_client):
        data=old_task_info.copy()
        data["status"] = "not_a_status"
        response = authenticated_client.put(
            update_delete_url, data=data, content_type="application/json"
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_update_todo_invalid_priority(self,old_task_info,update_delete_url,authenticated_client):
        data=old_task_info.copy()
        data["priority"] = "urgent"
        response = authenticated_client.put(
            update_delete_url, data=data, content_type="application/json"
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_update_todo_invalid_due_date_format(self,old_task_info,update_delete_url,authenticated_client):
        data=old_task_info.copy()
        data["duo_date"] = "not-a-date"
        response = authenticated_client.put(
            update_delete_url, data=data, content_type="application/json"
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST

# test partial update task successfull
    def test_partial_update_todo(self,old_task_info,update_delete_url,authenticated_client):
        partial_payload = {"title": "test - partial update", "status": "completed"}
        response = authenticated_client.put(
            update_delete_url, data=partial_payload, content_type="application/json"
        )
        data=old_task_info.copy()
        assert response.status_code == status.HTTP_200_OK
        assert response.data.get("title") == "test - partial update"
        assert response.data.get("status") == "completed"
        assert response.data.get("duo_date") == data["duo_date"] + "T00:00:00Z"
        assert response.data.get("priority") == data["priority"]
        assert response.data.get("description") == data["description"]


# delete tasks test class
@pytest.mark.django_db
class TestDeleteTodo:
    def test_delete_todo(self,update_delete_url,authenticated_client):
        response = authenticated_client.delete(update_delete_url)
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_delete_non_existent_todo(self,update_delete_url,authenticated_client):
        non_existent_url = reverse("update_delete_tasks", args=[3])
        response = authenticated_client.delete(non_existent_url)
        assert response.status_code == status.HTTP_404_NOT_FOUND
