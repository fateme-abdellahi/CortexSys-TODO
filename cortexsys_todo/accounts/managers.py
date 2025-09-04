from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    """
    create user manager.
    username, email and password are required fields for both user and superuser.
    """
    
    # Create a regular user
    def create_user(self, username, email, password, **extra_fields):
        if not username:
            raise ValueError("The Username is required")
        if not email:
            raise ValueError("The Email is required")
        if not password:
            raise ValueError("Password is required")

        user = self.model(username=username, password=password, email=email)
        user.set_password(password)
        user.save()
        return user

    # Create a superuser
    def create_superuser(self, username, email, password, **extra_fields):
        if not username:
            raise ValueError("The Username is required")
        if not email:
            raise ValueError("The Email is required")
        if not password:
            raise ValueError("Password is required")

        user = self.model(
            username=username,
            password=password,
            email=email,
            is_staff=True,
            is_superuser=True,
        )
        user.set_password(password)
        user.save()
        return user
