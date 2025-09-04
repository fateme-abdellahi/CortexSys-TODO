from .models import CustomUser
from rest_framework import serializers


class RegisterSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.
    Validates password, password confirmation (password2), and email uniqueness.
    """

    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    email = serializers.EmailField(required=True)

    class Meta:
        model = CustomUser
        fields = ("username", "password", "password2", "email")

    # Validate password length
    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError(
                "Password must be at least 8 characters long."
            )
        return value

    # Ensure password and password2 match
    def validate_password2(self, value):
        if self.initial_data["password"] != value:
            raise serializers.ValidationError("Passwords do not match.")
        return value

    # Ensure email is unique
    def validate_email(self, value):
        if CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists")
        return value

    # Create the user with username, password and email; if validation passes
    def create(self, validated_data):
        username = validated_data["username"]
        password = validated_data["password"]
        email = validated_data["email"]
        user = CustomUser.objects.create_user(
            username=username, email=email, password=password
        )
        return user
