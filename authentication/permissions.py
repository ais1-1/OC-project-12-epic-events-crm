from rest_framework import permissions

from teams.models import Team


class UserPermissions(permissions.BasePermission):
    """
    Allow only management team users to create, access, update or delete user data.
    """

    def has_permission(self, request, view):
        # Connected user is from management team
        return request.user.role == Team.get_management_team()
