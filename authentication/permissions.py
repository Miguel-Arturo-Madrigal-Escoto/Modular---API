from rest_framework.permissions import BasePermission
from django.forms.models import model_to_dict

class ProfilePermissions(BasePermission):
       
    def has_object_permission(self, request, view, obj):
        print(request.user.id == obj.user.id)
        print(obj.user.email)
        return request.user.id == obj.user.id