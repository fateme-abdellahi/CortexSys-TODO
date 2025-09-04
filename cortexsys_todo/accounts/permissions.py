from rest_framework import permissions


# allow all users to access the registration endpoint
class RegisterPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return True
