from rest_framework import permissions

class IsTaskOwnerOrAdmin(permissions.BasePermission):
    """
    Custom permission to only allow owner of the task or admins to view, create, update, or delete it.
    """
    
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user or request.user.is_staff
