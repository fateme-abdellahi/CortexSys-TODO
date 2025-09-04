from .models import Task
from rest_framework import serializers


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        exclude = ["user"]
        read_only_fields = ["created_at", "updated_at"]

    def get_fields(self):
        fields = super().get_fields()
        if self.instance:
            for field in fields.values():
                field.required = False
        return fields

    def create(self, validated_data):
        user = self.context["request"].user
        validated_data["user"] = user
        if Task.objects.filter(user=user, title=validated_data["title"]).exists():
            raise serializers.ValidationError("A task with this title already exists.")
        return Task.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get("title", instance.title)
        instance.description = validated_data.get("description", instance.description)
        instance.status = validated_data.get("status", instance.status)
        instance.duo_date = validated_data.get("duo_date", instance.duo_date)
        instance.priority = validated_data.get("priority", instance.priority)
        instance.save()

        return instance
