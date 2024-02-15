import pytest
import datetime
from django.urls import reverse
from rest_framework import status

from .models import Event


@pytest.mark.django_db
class TestEventsModels:

    def test_event_str(self, event):
        assert str(event) == f"{event.id}: {event.name} - {event.status}"

    def test_client_details(self, event, signed_contract):
        assert event.client_name == signed_contract.client.full_name
        assert event.client_phone == "Data unavailable."
        assert event.client_email == signed_contract.client.email


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
        print(response)
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
