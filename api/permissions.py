from rest_framework import permissions


class EmployeePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.type == "Сотрудник"
