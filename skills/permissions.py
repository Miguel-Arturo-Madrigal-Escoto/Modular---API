from rest_framework.permissions import BasePermission


class SkillsPermissions(BasePermission):
    def has_permission(self, request, view):
        return super().has_permission(request, view)

    def has_object_permission(self, request, view, obj):
        try:
            return request.user.user and request.user.user.id == obj.user.id
        except Exception:
            return False
