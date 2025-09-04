from .models import Task
from rest_framework import serializers


class TaskSerializer(serializers.ModelSerializer):
    """
    Serializer for Task model.
    """

    class Meta:
        model = Task

        # Exclude the user field and makes created_at and updated_at read-only
        exclude = ["user"]
        read_only_fields = ["created_at", "updated_at"]

    def get_fields(self):
        # Make all fields optional for updates
        fields = super().get_fields()
        if self.instance:
            for field in fields.values():
                field.required = False
        return fields

    def create(self, validated_data):

        # get the authenticated user from the request context and add to serialized data
        user = self.context["request"].user
        validated_data["user"] = user

        # ensure the user does not already have a task with the same title
        if Task.objects.filter(user=user, title=validated_data["title"]).exists():
            raise serializers.ValidationError("A task with this title already exists.")
        return Task.objects.create(**validated_data)

    def update(self, instance, validated_data):
        # update only the fields provided in the request
        instance.title = validated_data.get("title", instance.title)
        instance.description = validated_data.get("description", instance.description)
        instance.status = validated_data.get("status", instance.status)
        instance.duo_date = validated_data.get("duo_date", instance.duo_date)
        instance.priority = validated_data.get("priority", instance.priority)
        instance.save()

        return instance
