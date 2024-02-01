import pytest
import secrets

from authentication.models import User
from teams.models import Team
from .models import Client


@pytest.mark.django_db
class TestClientsModels:
    def setup_method(self):
        """Create a Client instance"""
        self.sales_user = User.objects.create_user(
            email=f"{secrets.token_hex(10)}@{secrets.token_hex(10)}.com",
            password=secrets.token_hex(10),
            first_name=secrets.token_hex(10),
            last_name=secrets.token_hex(10),
            role=Team.get_sales_team(),
        )
        self.client = Client.objects.create(
            email=f"{secrets.token_hex(10)}@{secrets.token_hex(10)}.com",
            first_name=secrets.token_hex(10),
            last_name=secrets.token_hex(10),
            sales_contact=self.sales_user,
        )
        self.client_without_contact = Client.objects.create(
            email=f"{secrets.token_hex(10)}@{secrets.token_hex(10)}.com",
            first_name=secrets.token_hex(10),
            last_name=secrets.token_hex(10),
        )

    def test_client_str(self):
        assert (
            str(self.client)
            == f"{self.client.id}: {self.client.last_name} {self.client.first_name}; "
            + f"contact: {self.client.sales_contact.full_name} "
        )
        assert (
            str(self.client_without_contact)
            == f"{self.client_without_contact.id}: "
            + f"{self.client_without_contact.last_name} "
            + f"{self.client_without_contact.first_name}; No sales contact yet..."
        )

    def test_full_name_property(self):
        assert (
            self.client.full_name == f"{self.client.last_name} {self.client.first_name}"
        )
