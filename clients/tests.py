import pytest
from django.urls import reverse
from rest_framework import status

from .models import Client


@pytest.mark.django_db
class TestClientsModels:
    def test_client_str(self, epic_client, client_without_contact):
        assert (
            str(epic_client)
            == f"{epic_client.id}: {epic_client.last_name} {epic_client.first_name}; "
            + f"contact: {epic_client.sales_contact.full_name} "
        )
        assert (
            str(client_without_contact)
            == f"{client_without_contact.id}: "
            + f"{client_without_contact.last_name} "
            + f"{client_without_contact.first_name}; No sales contact yet..."
        )

    def test_full_name_property(self, epic_client):
        assert (
            epic_client.full_name == f"{epic_client.last_name} {epic_client.first_name}"
        )


@pytest.mark.django_db
class TestClientViews:
    def setup_method(self):
        self.CLIENT_LIST_URL = reverse("clients-list")

    def test_sales_user_list_access(self, sales_user, sales_user_authenticated_client):
        response = sales_user_authenticated_client.get(self.CLIENT_LIST_URL)
        assert response.status_code == status.HTTP_200_OK

    def test_superuser_list_access(self, superuser, superuser_authenticated_client):
        response = superuser_authenticated_client.get(self.CLIENT_LIST_URL)
        assert response.status_code == status.HTTP_200_OK

    def test_superuser_create_access(self, superuser, superuser_authenticated_client):
        response = superuser_authenticated_client.post(self.CLIENT_LIST_URL)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_sales_user_create_client(
        self, sales_user, sales_user_authenticated_client
    ):
        data = {
            "email": "test@email.com",
            "first_name": "Toto",
            "last_name": "TEST",
        }
        response = sales_user_authenticated_client.post(self.CLIENT_LIST_URL, data)
        client_created = Client.objects.get(email=data["email"])
        assert response.status_code == status.HTTP_201_CREATED
        assert client_created is not None
        assert client_created.sales_contact == sales_user
