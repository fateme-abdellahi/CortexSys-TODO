from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, mixins
from .models import Task
from .serializers import TaskSerializer
from .permissions import IsTaskOwnerOrAdmin


class TasksListCreateView(generics.ListCreateAPIView):
    """
    In this class authenticated users can view all of their own tasks or create a new task
    """

    permission_classes = [IsTaskOwnerOrAdmin]
    serializer_class = TaskSerializer

    # filter tasks by status and priority in query params
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["status", "priority"]

    # get all the user's tasks for the authenticated user, or all users tasks if the user is an admin
    def get_queryset(self):
        if self.request.user.is_staff:
            return Task.objects.all()
        return Task.objects.filter(user=self.request.user)


class TaskUpdateDeleteView(
    mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView
):
    """
    In this class authenticated users can update their own task or delete the task.
    The task is identified by its ID in the URL.
    """

    permission_classes = [IsTaskOwnerOrAdmin]
    serializer_class = TaskSerializer

    def get_queryset(self):
        if self.request.user.is_staff:
            return Task.objects.all()
        return Task.objects.filter(user=self.request.user)

    # update the task
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    # delete the task
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
