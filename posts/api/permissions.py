from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsOwnerOrReadOnly(BasePermission):
	message = 'You must be the owner of this object'
	# my_self_method = ['PUT', 'GET']
	# def has_permission(self, request, view):
	# 	if request.method in self.my_self_method:
	# 		return True
	# 	return False

	def has_object_permission(self, request, view,obj):
		if request.method in SAFE_METHODS:
			return True
		return obj.user == request.user