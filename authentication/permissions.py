from rest_framework.permissions import BasePermission
from .models import BaseUser

class UserPermissions(BasePermission):
    
    def has_permission(self, request, view):
        return super().has_permission(request, view)
       
    def has_object_permission(self, request, view, obj):
        """
        Check if authenticted user has 'user' (not company) role and match both ids.
        """
        try:
            return not request.user.user and request.user.id == obj.base_user.id
        except Exception:
            return False
        

class CompanyPermissions(BasePermission):

    def has_permission(self, request, view):
        return super().has_permission(request, view)
    
    def has_object_permission(self, request, view, obj):
        """
        Check if authenticted user has 'company' role and match both ids.
        """
        try:
            return request.user.company and request.user.id == obj.base_user.id
        except Exception:
            return False