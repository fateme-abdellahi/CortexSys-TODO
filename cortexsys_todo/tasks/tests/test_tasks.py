from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse


class TodoCreationTest(APITestCase):
    def setUp(self):
        response = self.client.post(
            reverse("register"),
            {
                "username": "test",
                "password": "11111111",
                "password2": "11111111",
                "email": "test@email.com",
            },
            format="json",
        )

        self.client.credentials(
            HTTP_AUTHORIZATION="Bearer " + response.data.get("tokens").get("access")
        )
        self.url = reverse("list_create_tasks")

    def test_create_todo_missing_title(self):
        response = self.client.post(
            self.url,
            {"description": "desc", "status": "pending", "priority": "medium"},
            format="json",
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_todo_invalid_status(self):
        response = self.client.post(
            self.url,
            {"title": "test", "status": "not_a_status"},
            content_type="application/json",
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_todo_invalid_priority(self):
        response = self.client.post(
            self.url,
            {"title": "test", "priority": "urgent"},
            content_type="application/json",
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_todo_invalid_due_date_format(self):
        response = self.client.post(
            self.url,
            {"title": "test", "duo_date": "not-a-date"},
            content_type="application/json",
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_todo_empty_payload(self):
        response = self.client.post(self.url, {}, content_type="application/json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_todo_long_title(self):
        long_title = "t" * 300
        response = self.client.post(
            self.url, {"title": long_title}, content_type="application/json"
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_todo_duplicate_title(self):
        self.client.post(
            self.url, {"title": "unique-title"}, content_type="application/json"
        )
        response = self.client.post(
            self.url, {"title": "unique-title"}, content_type="application/json"
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST


class todoUpdateTest(APITestCase):
    def setUp(self):

        response = self.client.post(
            reverse("register"),
            {
                "username": "test",
                "password": "11111111",
                "password2": "11111111",
                "email": "test@email.com",
            },
        )
        self.client.credentials(
            HTTP_AUTHORIZATION="Bearer " + response.data.get("tokens").get("access")
        )

        self.payload = {
            "title": "test task",
            "description": "test description",
            "status": "pending",
            "priority": "medium",
            "duo_date": "2025-01-01",
        }

        response = self.client.post(
            reverse("list_create_tasks"),
            data=self.payload,
            content_type="application/json",
        )
        self.url = reverse("update_delete_tasks", args=[response.data.get("id")])

    def test_update_todo(self):
        self.payload["title"] = "test - updated"
        self.payload["status"] = "completed"
        self.payload["duo_date"] = "2025-01-02"
        self.payload["priority"] = "high"
        self.payload["description"] = "updated description"
        response = self.client.put(
            self.url, data=self.payload, content_type="application/json"
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.data.get("title") == "test - updated"
        assert response.data.get("status") == "completed"
        assert response.data.get("duo_date") == "2025-01-02T00:00:00Z"
        assert response.data.get("priority") == "high"
        assert response.data.get("description") == "updated description"

    def test_update_todo_invalid_status(self):
        self.payload["status"] = "not_a_status"
        response = self.client.put(
            self.url, data=self.payload, content_type="application/json"
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_update_todo_invalid_priority(self):
        self.payload["priority"] = "urgent"
        response = self.client.put(
            self.url, data=self.payload, content_type="application/json"
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_update_todo_invalid_due_date_format(self):
        self.payload["duo_date"] = "not-a-date"
        response = self.client.put(
            self.url, data=self.payload, content_type="application/json"
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_partial_update_todo(self):
        partial_payload = {"title": "test - partial update", "status": "completed"}
        response = self.client.put(
            self.url, data=partial_payload, content_type="application/json"
        )
        assert response.data.get("title") == "test - partial update"
        assert response.data.get("status") == "completed"
        assert response.data.get("duo_date") == self.payload["duo_date"] + "T00:00:00Z"
        assert response.data.get("priority") == self.payload["priority"]
        assert response.data.get("description") == self.payload["description"]


class todoDeleteTest(APITestCase):
    def setUp(self):

        response = self.client.post(
            reverse("register"),
            {
                "username": "test",
                "password": "11111111",
                "password2": "11111111",
                "email": "test@email.com",
            },
        )
        self.client.credentials(
            HTTP_AUTHORIZATION="Bearer " + response.data.get("tokens").get("access")
        )

        self.payload = {
            "title": "test task",
            "description": "test description",
            "status": "pending",
            "priority": "medium",
            "duo_date": "2025-01-01",
        }

        response = self.client.post(
            reverse("list_create_tasks"),
            data=self.payload,
            content_type="application/json",
        )
        self.url = reverse("update_delete_tasks", args=[response.data.get("id")])

    def test_delete_todo(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_non_existent_todo(self):
        non_existent_url = reverse("update_delete_tasks", args=[3])
        response = self.client.delete(non_existent_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
