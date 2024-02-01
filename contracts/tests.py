import pytest
import secrets

from authentication.models import User
from teams.models import Team
from clients.models import Client
from .models import Contract


@pytest.mark.django_db
class TestContractsModels:
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
        self.signed_contract = Contract.objects.create(
            total_amount=1500, signed=True, client=self.client
        )
        self.unsigned_contract = Contract.objects.create(
            total_amount=1500, signed=False, client=self.client_without_contact
        )
        self.contract_without_client = Contract.objects.create(
            total_amount=1500, signed=False, sales_contact=self.sales_user
        )

    def test_contract_str(self):
        assert (
            str(self.signed_contract)
            == f"{self.signed_contract.id}: Contract signed - "
            + f"{self.signed_contract.client.full_name}"
        )
        assert (
            str(self.unsigned_contract)
            == f"{self.unsigned_contract.id}: Contract not signed - "
            + f"{self.unsigned_contract.client.full_name}"
        )
        assert (
            str(self.contract_without_client)
            == f"{self.contract_without_client.id}: Contract not signed - "
            + "Client info is unavailable"
        )

    def test_save_with_sales_contact_if_not_provided(self):
        assert self.signed_contract.sales_contact == self.sales_user
        assert self.unsigned_contract.sales_contact is None
        assert self.contract_without_client.sales_contact == self.sales_user
