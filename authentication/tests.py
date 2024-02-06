import pytest
import secrets


from teams.models import Team


@pytest.mark.django_db
class TestAuthenticationModels:
    """def setup_method(self):
    Create a User instance
    self.superuser = User.objects.create_superuser(
        email=f"{secrets.token_hex(10)}@{secrets.token_hex(10)}.com",
        password=secrets.token_hex(10),
        first_name=secrets.token_hex(10),
        last_name=secrets.token_hex(10),
    )"""

    @pytest.mark.usefixtures("superuser")
    def test_user_str(self, superuser):
        """
        Testing if User's __str__ method is properly implemented
        """

        assert (
            str(superuser)
            == f"{superuser.id}: {superuser.full_name} ({superuser.email})"
        )

    @pytest.mark.usefixtures("superuser")
    def test_superuser_default_role(self, superuser):
        assert superuser.role == Team.get_management_team()

    def test_create_user_without_email(self, django_user_model):
        with pytest.raises(TypeError):
            self.user_without_email = django_user_model.objects.create_user(
                password=secrets.token_hex(10),
                first_name=secrets.token_hex(10),
                last_name=secrets.token_hex(10),
                role=Team.get_sales_team(),
            )
