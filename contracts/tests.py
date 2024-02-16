import pytest
from django.urls import reverse
from rest_framework import status
from django.http import HttpResponseNotFound

from .models import Contract
from events.models import Event


@pytest.mark.django_db
class TestContractsModels:
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
        self.OWN_ACTION_URL = self.CONTRACT_LIST_URL + "own/"
        self.UNSIGNED_ACTION_URL = self.CONTRACT_LIST_URL + "unsigned/"
        self.UNPAID_ACTION_URL = self.CONTRACT_LIST_URL + "unpaid/"
        self.SIGNED_ACTION_URL = self.CONTRACT_LIST_URL + "signed/"
        self.WITHOUT_EVENT_ACTION_URL = self.CONTRACT_LIST_URL + "without_event/"

    def test_sales_user_list_access(self, sales_user, sales_user_authenticated_client):
        response = sales_user_authenticated_client.get(self.CONTRACT_LIST_URL)
        assert response.status_code == status.HTTP_200_OK

    def test_superuser_list_access(self, superuser, superuser_authenticated_client):
        response = superuser_authenticated_client.get(self.CONTRACT_LIST_URL)
        assert response.status_code == status.HTTP_200_OK

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

    def test_sales_user_create(self, sales_user, sales_user_authenticated_client):

        response = sales_user_authenticated_client.post(self.CONTRACT_LIST_URL)
        assert response.status_code == status.HTTP_403_FORBIDDEN

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
        assert response.status_code == HttpResponseNotFound.status_code
        assert has_unpaid_contract is False

    def test_unpaid_contract_not_empty_list(
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

    def test_own_action_no_contracts(self, sales_user, sales_user_authenticated_client):
        response = sales_user_authenticated_client.get(self.OWN_ACTION_URL)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_own_action_with_contracts(
        self, sales_user, signed_contract, sales_user_authenticated_client
    ):
        response = sales_user_authenticated_client.get(self.OWN_ACTION_URL)
        response_dict = response.json()
        assert response.status_code == status.HTTP_200_OK
        assert response_dict[0]["sales_contact"] == sales_user.id
        assert response_dict[0]["id"] == str(signed_contract.id)

    def test_unsigned_no_contracts(self, sales_user, sales_user_authenticated_client):
        response = sales_user_authenticated_client.get(self.UNSIGNED_ACTION_URL)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_unsigned_with_contracts(
        self, sales_user, unsigned_contract, sales_user_authenticated_client
    ):
        response = sales_user_authenticated_client.get(self.UNSIGNED_ACTION_URL)
        response_dict = response.json()
        assert response.status_code == status.HTTP_200_OK
        assert response_dict[0]["sales_contact"] == sales_user.id
        assert response_dict[0]["id"] == str(unsigned_contract.id)
        assert response_dict[0]["signed"] is False

    def test_signed_no_contracts(self, sales_user, sales_user_authenticated_client):
        response = sales_user_authenticated_client.get(self.SIGNED_ACTION_URL)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_signed_with_contracts(
        self, sales_user, signed_contract, sales_user_authenticated_client
    ):
        response = sales_user_authenticated_client.get(self.SIGNED_ACTION_URL)
        response_dict = response.json()
        assert response.status_code == status.HTTP_200_OK
        assert response_dict[0]["sales_contact"] == sales_user.id
        assert response_dict[0]["id"] == str(signed_contract.id)
        assert response_dict[0]["signed"] is True

    def test_unpaid_no_contracts(self, sales_user, sales_user_authenticated_client):
        response = sales_user_authenticated_client.get(self.UNPAID_ACTION_URL)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_unpaid_with_contracts(
        self, sales_user, unpaid_contract, sales_user_authenticated_client
    ):
        response = sales_user_authenticated_client.get(self.UNPAID_ACTION_URL)
        response_dict = response.json()
        assert response.status_code == status.HTTP_200_OK
        assert response_dict[0]["sales_contact"] == sales_user.id
        assert response_dict[0]["id"] == str(unpaid_contract.id)
        assert float(response_dict[0]["amount_due"]) > 0.00

    def test_without_event_no_contracts(
        self, sales_user, sales_user_authenticated_client
    ):
        response = sales_user_authenticated_client.get(self.WITHOUT_EVENT_ACTION_URL)
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_without_event_with_signed_contract(
        self, sales_user, signed_contract, sales_user_authenticated_client
    ):
        response = sales_user_authenticated_client.get(self.WITHOUT_EVENT_ACTION_URL)
        response_dict = response.json()
        events = Event.objects.all()
        signed_contract_has_event = False
        for event in events:
            if event.contract.id == signed_contract.id:
                signed_contract_has_event = True
        assert response.status_code == status.HTTP_200_OK
        assert signed_contract_has_event is False
        assert response_dict[0]["sales_contact"] == sales_user.id
        assert response_dict[0]["id"] == str(signed_contract.id)
        assert response_dict[0]["signed"] is True
