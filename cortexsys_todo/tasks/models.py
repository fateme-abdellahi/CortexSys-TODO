from django.db import models
from accounts.models import CustomUser


class Task(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="tasks")
    title = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(
        max_length=15,
        choices=[
            ("pending", "pending"),
            ("completed", "completed"),
        ],
        default="pending",
    )
    duo_date = models.DateTimeField(blank=True, null=True)
    priority = models.CharField(
        max_length=50,
        choices=[
            ("low", "low"),
            ("medium", "medium"),
            ("high", "high"),
        ],
        default="medium",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
