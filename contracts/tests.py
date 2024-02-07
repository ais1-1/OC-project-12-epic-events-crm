import pytest
from django.urls import reverse
from rest_framework import status

from .models import Contract


@pytest.mark.django_db
class TestContractsModels:
    @pytest.mark.usefixtures(
        "signed_contract",
        "unsigned_contract_without_contact",
        "unsigned_contract_without_client",
    )
    def test_contract_str(
        self,
        signed_contract,
        unsigned_contract_without_client,
        unsigned_contract_without_contact,
    ):
        assert (
            str(signed_contract)
            == f"{signed_contract.id}: Contract signed - "
            + f"{signed_contract.client.full_name}"
        )
        assert (
            str(unsigned_contract_without_contact)
            == f"{unsigned_contract_without_contact.id}: Contract not signed - "
            + f"{unsigned_contract_without_contact.client.full_name}"
        )
        assert (
            str(unsigned_contract_without_client)
            == f"{unsigned_contract_without_client.id}: Contract not signed - "
            + "Client info is unavailable"
        )

    @pytest.mark.usefixtures(
        "signed_contract",
        "unsigned_contract_without_contact",
        "unsigned_contract_without_client",
        "sales_user",
    )
    def test_save_with_sales_contact_if_not_provided(
        self,
        sales_user,
        signed_contract,
        unsigned_contract_without_client,
        unsigned_contract_without_contact,
    ):
        assert signed_contract.sales_contact == sales_user
        assert unsigned_contract_without_contact.sales_contact is None
        assert unsigned_contract_without_client.sales_contact == sales_user


@pytest.mark.django_db
class TestContractsViews:
    def setup_method(self):
        self.CONTRACT_LIST_URL = reverse("contracts-list")

    @pytest.mark.usefixtures("sales_user", "sales_user_authenticated_client")
    def test_sales_user_list_access(self, sales_user, sales_user_authenticated_client):
        response = sales_user_authenticated_client.get(self.CONTRACT_LIST_URL)
        assert response.status_code == status.HTTP_200_OK

    @pytest.mark.usefixtures("superuser", "superuser_authenticated_client")
    def test_superuser_list_access(self, superuser, superuser_authenticated_client):
        response = superuser_authenticated_client.get(self.CONTRACT_LIST_URL)
        assert response.status_code == status.HTTP_200_OK

    @pytest.mark.usefixtures("superuser", "superuser_authenticated_client")
    def test_superuser_create(
        self, superuser, superuser_authenticated_client, epic_client
    ):
        data = {
            "total_amount": 20000,
            "client": epic_client.pk,
            "amount_due": 500,
        }

        response = superuser_authenticated_client.post(self.CONTRACT_LIST_URL, data)
        created_contract_id = response.data.get("id")
        created_contract = Contract.objects.get(id=created_contract_id)
        assert response.status_code == status.HTTP_201_CREATED
        assert created_contract.signed is False
        assert created_contract.sales_contact == epic_client.sales_contact

    @pytest.mark.usefixtures("sales_user", "sales_user_authenticated_client")
    def test_sales_user_create(self, sales_user, sales_user_authenticated_client):

        response = sales_user_authenticated_client.post(self.CONTRACT_LIST_URL)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.usefixtures(
        "sales_user", "sales_user_authenticated_client", "signed_contract"
    )
    def test_sales_user_contact_patch(
        self, sales_user, sales_user_authenticated_client, signed_contract
    ):
        new_amount_due_data = 200.00
        current_amount_due = signed_contract.amount_due
        sales_contact = signed_contract.sales_contact
        response = sales_user_authenticated_client.patch(
            self.CONTRACT_LIST_URL + f"{signed_contract.id}/",
            data={"amount_due": new_amount_due_data},
            format="json",
        )
        new_amount_due = response.data.get("amount_due")
        assert response.status_code == status.HTTP_200_OK
        assert current_amount_due is not new_amount_due
        assert new_amount_due == "{:.2f}".format(new_amount_due_data)
        assert sales_user == sales_contact

    @pytest.mark.usefixtures(
        "sales_user2", "sales_user2_authenticated_client", "signed_contract"
    )
    def test_sales_user_not_contact_patch(
        self, sales_user2, sales_user2_authenticated_client, signed_contract
    ):
        new_amount_due_data = 100.00
        sales_contact = signed_contract.sales_contact
        response = sales_user2_authenticated_client.patch(
            self.CONTRACT_LIST_URL + f"{signed_contract.id}/",
            data={"amount_due": new_amount_due_data},
            format="json",
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert sales_contact is not sales_user2

    @pytest.mark.usefixtures(
        "sales_user",
        "sales_user_authenticated_client",
        "signed_contract",
        "signed_contract2",
    )
    def test_unpaid_contract_empty_list(
        self,
        sales_user,
        sales_user_authenticated_client,
    ):
        has_unpaid_contract = True
        if (
            Contract.objects.filter(
                sales_contact=sales_user, amount_due__gt=0.00
            ).count()
            == 0
        ):
            has_unpaid_contract = False
        response = sales_user_authenticated_client.get(
            self.CONTRACT_LIST_URL + "unpaid/"
        )
        assert response.status_code == status.HTTP_200_OK
        assert has_unpaid_contract is False
        assert len(response.data) == 0

    @pytest.mark.usefixtures(
        "sales_user",
        "sales_user_authenticated_client",
        "signed_contract",
        "signed_contract2",
    )
    def test_unpaid_contract_unempty_list(
        self,
        sales_user2,
        sales_user2_authenticated_client,
        signed_contract2,
    ):
        has_unpaid_contract = True
        if (
            Contract.objects.filter(
                sales_contact=sales_user2, amount_due__gt=0.00
            ).count()
            == 0
        ):
            has_unpaid_contract = False
        response = sales_user2_authenticated_client.get(
            self.CONTRACT_LIST_URL + "unpaid/"
        )
        assert response.status_code == status.HTTP_200_OK
        assert has_unpaid_contract is True
        assert len(response.data) > 0
        assert response.data[0]["amount_due"] == "{:.2f}".format(
            signed_contract2.amount_due
        )
