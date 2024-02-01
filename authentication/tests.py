import pytest
import secrets


from teams.models import Team
from .models import User


@pytest.mark.django_db
class TestAuthenticationModels:
    def setup_method(self):
        """Create a User instance"""
        self.superuser = User.objects.create_superuser(
            email=f"{secrets.token_hex(10)}@{secrets.token_hex(10)}.com",
            password=secrets.token_hex(10),
            first_name=secrets.token_hex(10),
            last_name=secrets.token_hex(10),
        )

    def test_user_str(self):
        """
        Testing if User's __str__ method is properly implemented
        """

        assert (
            str(self.superuser)
            == f"{self.superuser.id}: {self.superuser.full_name} ({self.superuser.email})"
        )

    def test_superuser_default_role(self):
        assert self.superuser.role == Team.get_management_team()

    def test_create_user_without_email(self):
        with pytest.raises(TypeError):
            self.user_without_email = User.objects.create_user(
                password=secrets.token_hex(10),
                first_name=secrets.token_hex(10),
                last_name=secrets.token_hex(10),
                role=Team.get_sales_team(),
            )
