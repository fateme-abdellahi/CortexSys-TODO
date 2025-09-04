from rest_framework import permissions

# Registration is open, but other endpoints should be protected
class RegisterPermission(permissions.BasePermission):
	def has_permission(self, request, view):
		# Allow registration without authentication
		return True
