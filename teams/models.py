from django.db import models
from django.core.exceptions import PermissionDenied

SALES = "SALES"
SUPPORT = "SUPPORT"
MANAGEMENT = "MANAGEMENT"

TEAM_LIMIT = 3


class Team(models.Model):
    """
    Team model

    The instances are created during migration see the second migration file in migrations/.

    Attributes:
    name (str): name of the team
    description (str): description of the team
    created_date (str): Date of creation of an instance

    Methods:
    save - prevent creation and update if there are more team that TEAM_LIMIT
    delete - prevent deletion
    get_management_team (static) - returns management team object
    get_sales_team (static) - returns sales team object
    get_support_team (static) - returns support team object
    """

    name = models.CharField(max_length=255)
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Team"
        verbose_name_plural = "Teams"
        db_table = "team"
        # Last created item first
        ordering = ("-created_date",)

    def __str__(self):
        return f"{self.name}"

    def save(self, *args, **kwargs):
        """Prevent from creating new teams or editing existing teams."""
        if Team.objects.all().count() >= TEAM_LIMIT or self.pk is not None:
            raise PermissionDenied("You are not permitted to create team")

    def delete(self, using=None, keep_parents=False):
        """Prevent from deleting teams."""
        raise PermissionDenied("You are not allowed to delete teams.")

    @staticmethod
    def get_management_team():
        return Team.objects.get(id=1)

    @staticmethod
    def get_sales_team():
        return Team.objects.get(id=2)

    @staticmethod
    def get_support_team():
        return Team.objects.get(id=3)
