from django.db import models
from accounts.models import CustomUser


class Task(models.Model):
    """Model representing a task."""

    # Each task is associated with a user
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="tasks")

    title = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)

    # Task can be either pending or completed
    status = models.CharField(
        max_length=15,
        choices=[
            ("pending", "pending"),
            ("completed", "completed"),
        ],
        default="pending",
    )
    duo_date = models.DateTimeField(blank=True, null=True)

    # Task can have low, medium, or high priority
    priority = models.CharField(
        max_length=50,
        choices=[
            ("low", "low"),
            ("medium", "medium"),
            ("high", "high"),
        ],
        default="medium",
    )
    # automatically set the field to now when the object is first created
    created_at = models.DateTimeField(auto_now_add=True)

    # automatically set the field to now every time the object is saved
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
