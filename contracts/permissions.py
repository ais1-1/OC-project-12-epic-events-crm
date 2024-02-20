from rest_framework import permissions

from teams.models import Team


class ContractPermissions(permissions.BasePermission):
    """
    Read access to all collaborators.
    All access to management team.
    Update access to contracts sales contact.
    """

    def has_permission(self, request, view):
        edit_methods = ["PUT", "PATCH"]

        if request.method in permissions.SAFE_METHODS:
            return True

        if request.user.role == Team.get_management_team():
            return True

        if request.method in edit_methods:
            return request.user.role == Team.get_sales_team()

    def has_object_permission(self, request, view, obj):
        edit_methods = ["PUT", "PATCH"]

        if request.method in permissions.SAFE_METHODS:
            return True

        if request.user.role == Team.get_management_team():
            return True

        if request.method in edit_methods:
            return request.user == obj.sales_contact

        return False
