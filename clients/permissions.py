from rest_framework import permissions

from teams.models import Team


class ClientPermissions(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return request.user.role.name == Team.get_sales_team().name
