from rest_framework.permissions import BasePermission


class CompanyRolesPermissions(BasePermission):
    def has_permission(self, request, view):
        try:
            return request.user.company
        except Exception:
            return False

    def has_object_permission(self, request, view, obj):
        try:
            return request.user.company and request.user.company.id == obj.company.id
        except Exception:
            return False
