from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, mixins
from .models import Task
from .serializers import TaskSerializer
from rest_framework import permissions

class TasksListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TaskSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status', 'priority']
    
    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)
    
class TaskUpdateDeleteView(mixins.UpdateModelMixin,mixins.DestroyModelMixin,generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TaskSerializer

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)