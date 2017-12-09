
from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsStaffOrOwner(BasePermission):
	def has_permission(self, request, view):
		# allow user to list all users if logged in user is staff
		return view.action == 'retrieve' or 'create' or request.user.is_staff

	def has_object_permission(self, request, view, obj):
		return request.user.is_staff or request.user == obj.user_risktype

		

class IsStaffOrOwnerField(BasePermission):
	def has_permission(self, request, view):
		# allow user to list all users if logged in user is staff
		return view.action == 'retrieve' or 'create' or request.user.is_staff

	def has_object_permission(self, request, view, obj):
		return request.user.is_staff or request.user == obj.user_riskfield
		