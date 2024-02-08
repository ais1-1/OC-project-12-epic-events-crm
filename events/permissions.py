from rest_framework import permissions

from teams.models import Team


class EventPermissions(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        edit_methods = ["PUT", "PATCH"]

        if request.method in permissions.SAFE_METHODS:
            return True

        if request.method == "POST":
            print("in post obj perm")
            return request.user == obj.contract.client.sales_contact

        if request.method in edit_methods:
            return (
                request.user == obj.support_contact
                or request.user.role == Team.get_management_team()
            )

        return False