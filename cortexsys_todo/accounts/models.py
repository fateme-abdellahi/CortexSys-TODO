
from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import UserManager

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    objects = UserManager()
    