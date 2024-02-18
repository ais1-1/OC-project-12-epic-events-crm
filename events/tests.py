import pytest
import datetime
from django.urls import reverse
from rest_framework import status
from django.utils.timezone import make_aware

from .models import Event


@pytest.mark.django_db
class TestEventsModels:

    def test_event_str(self, event):
        assert str(event) == f"{event.id}: {event.name} - {event.status}"

    def test_client_details(self, event, signed_contract):
        assert event.client_name == signed_contract.client.full_name
        assert event.client_phone == "Data unavailable."
        assert event.client_email == signed_contract.client.email

    def test_event_without_client(self, signed_contract_without_client, support_user):
        event = Event.objects.create(
            name="testEvent",
            start_date=make_aware(datetime.datetime(2024, 3, 8)),
            end_date=make_aware(datetime.datetime(2024, 3, 10)),
            contract=signed_contract_without_client,
            support_contact=support_user,
        )
        assert event.contract.client is None
        assert event.client_name == "No client for the contract."
        assert event.client_email == "No client for the contract."
        assert event.client_phone == "No client for the contract."

    def test_event_with_client_phone(
        self, signed_contract2, epic_client2, support_user
    ):
        event = Event.objects.create(
            name="testEvent",
            start_date=make_aware(datetime.datetime(2024, 3, 8)),
            end_date=make_aware(datetime.datetime(2024, 3, 10)),
            contract=signed_contract2,
            support_contact=support_user,
        )
        assert event.contract.client is not None
        assert event.client_name == epic_client2.full_name
        assert event.client_email == epic_client2.email
        assert event.client_phone == epic_client2.phone


@pytest.mark.django_db
class TestEventsViews:
    def setup_method(self):
        self.EVENT_LIST_URL = reverse("events-list")

    def test_sales_user_list_access(self, sales_user, sales_user_authenticated_client):
        response = sales_user_authenticated_client.get(self.EVENT_LIST_URL)
        assert response.status_code == status.HTTP_200_OK

    def test_superuser_list_access(self, superuser, superuser_authenticated_client):
        response = superuser_authenticated_client.get(self.EVENT_LIST_URL)
        assert response.status_code == status.HTTP_200_OK

    def test_support_user_list_access(
        self, support_user, support_user_authenticated_client
    ):
        response = support_user_authenticated_client.get(self.EVENT_LIST_URL)
        assert response.status_code == status.HTTP_200_OK

    def test_sales_user_create(
        self, sales_user2, signed_contract2, sales_user2_authenticated_client
    ):
        data = {
            "name": "Concert",
            "start_date": datetime.datetime(2024, 5, 21),
            "end_date": datetime.datetime(2024, 5, 29),
            "contract": signed_contract2.id,
            "support_contact": "",
        }
        response = sales_user2_authenticated_client.post(self.EVENT_LIST_URL, data)
        created_event_id = response.data.get("id")
        created_event = Event.objects.get(id=created_event_id)

        assert response.status_code == status.HTTP_201_CREATED
        assert created_event is not None
        assert signed_contract2.sales_contact == sales_user2

    def test_sales_user_others_client_create(
        self, sales_user, signed_contract2, sales_user_authenticated_client
    ):
        data = {
            "name": "Concert1",
            "start_date": datetime.datetime(2025, 5, 21),
            "end_date": datetime.datetime(2025, 5, 29),
            "contract": signed_contract2.id,
        }
        response = sales_user_authenticated_client.post(self.EVENT_LIST_URL, data)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert signed_contract2.sales_contact is not sales_user

    def test_create_with_unsigned_contract(
        self, sales_user, sales_user_authenticated_client, unsigned_contract
    ):
        data = {
            "name": "Concert1",
            "start_date": datetime.datetime(2025, 5, 21),
            "end_date": datetime.datetime(2025, 5, 29),
            "contract": unsigned_contract.id,
        }
        response = sales_user_authenticated_client.post(self.EVENT_LIST_URL, data)
        response_dict = response.json()
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert (
            response_dict["message"]
            == "Please note that you can create an event only for signed contracts."
        )

    def test_create_forbidden(
        self, support_user, support_user_authenticated_client, unsigned_contract
    ):
        data = {
            "name": "Concert1",
            "start_date": datetime.datetime(2025, 5, 21),
            "end_date": datetime.datetime(2025, 5, 29),
            "contract": unsigned_contract.id,
        }
        response = support_user_authenticated_client.post(self.EVENT_LIST_URL, data)
        response_dict = response.json()
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert (
            response_dict["detail"]
            == "You do not have permission to perform this action."
        )

    def test_my_events_empty(
        self, sales_user2, signed_contract2, sales_user2_authenticated_client
    ):

        response = sales_user2_authenticated_client.get(
            self.EVENT_LIST_URL + "my_events/"
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_my_events(self, support_user, event, support_user_authenticated_client):

        response = support_user_authenticated_client.get(
            self.EVENT_LIST_URL + "my_events/"
        )
        response_dict = response.json()
        assert response.status_code == status.HTTP_200_OK
        assert Event.objects.filter(support_contact=support_user).count() > 0
        assert response_dict[0]["id"] == event.id

    def test_without_support_empty(
        self, sales_user2, signed_contract2, sales_user2_authenticated_client
    ):
        response = sales_user2_authenticated_client.get(
            self.EVENT_LIST_URL + "without_support/"
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_without_support(
        self,
        support_user,
        signed_contract2,
        support_user_authenticated_client,
        sales_user2_authenticated_client,
    ):

        data = {
            "name": "Concert",
            "start_date": datetime.datetime(2024, 5, 21),
            "end_date": datetime.datetime(2024, 5, 29),
            "contract": signed_contract2.id,
            "support_contact": "",
        }

        response1 = sales_user2_authenticated_client.post(self.EVENT_LIST_URL, data)
        response2 = sales_user2_authenticated_client.get(
            self.EVENT_LIST_URL + "without_support/"
        )
        created_event_id = response1.data.get("id")
        response_dict = response2.json()

        assert response2.status_code == status.HTTP_200_OK
        assert Event.objects.filter(support_contact__isnull=True).count() > 0
        assert response_dict[0]["id"] == created_event_id
