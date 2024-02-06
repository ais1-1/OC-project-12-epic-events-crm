import pytest
from django.core.exceptions import PermissionDenied


from .models import Team, MANAGEMENT, SALES, SUPPORT, TEAM_LIMIT


@pytest.mark.django_db
class TestTeamsModels:
    def setup_method(self):
        """Create a Team instance"""
        self.management_team = Team.objects.get(id=1)
        self.sales_team = Team.objects.get(id=2)
        self.support_team = Team.objects.get(id=3)

    def test_team_str(self):
        """
        Testing if Team's __str__ method is properly implemented
        """

        assert str(self.management_team) == MANAGEMENT
        assert str(self.sales_team) == SALES
        assert str(self.support_team) == SUPPORT

    def test_get_management_team(self):
        result = Team.get_management_team()
        expected = Team.objects.get(id=1)
        assert result == expected
        assert result.name == MANAGEMENT

    def test_get_sales_team(self):
        result = Team.get_sales_team()
        expected = Team.objects.get(id=2)
        assert result == expected
        assert result.name == SALES

    def test_get_support_team(self):
        result = Team.get_support_team()
        expected = Team.objects.get(id=3)
        assert result == expected
        assert result.name == SUPPORT

    def test_delete_team(self):
        team = Team.get_sales_team()
        with pytest.raises(PermissionDenied):
            team.delete()

    def test_create_new_team(self):
        with pytest.raises(PermissionDenied):
            Team.objects.create(name="TEST")

    def test_existing_team_count(self):
        assert Team.objects.all().count() == TEAM_LIMIT
