from rest_framework.permissions import BasePermission
from rest_framework.views import Request


class UsersPermission(BasePermission):
    def has_permission(self, request: Request, _):
        staff_methods = {"GET", "DELETE", "PATCH"}

        if request.method in staff_methods:
            return request.user.is_staff

        return True
