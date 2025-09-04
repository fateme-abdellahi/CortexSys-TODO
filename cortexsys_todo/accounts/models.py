from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import UserManager

# create custom user model with email as unique field
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    objects = UserManager()
