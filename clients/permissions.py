from rest_framework import permissions

from teams.models import Team


class ClientPermissions(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return request.user.role == Team.get_sales_team()

    def has_object_permission(self, request, view, obj):
        methods = ["PUT", "PATCH", "DELETE"]
        if request.method in methods:
            return request.user == obj.sales_contact

        if request.method in permissions.SAFE_METHODS:
            return True

        return False
