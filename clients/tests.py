import pytest
from django.urls import reverse
from rest_framework import status

from .models import Client


@pytest.mark.django_db
class TestClientsModels:
    @pytest.mark.usefixtures("client", "client_without_contact")
    def test_client_str(self, client, client_without_contact):
        assert (
            str(client)
            == f"{client.id}: {client.last_name} {client.first_name}; "
            + f"contact: {client.sales_contact.full_name} "
        )
        assert (
            str(client_without_contact)
            == f"{client_without_contact.id}: "
            + f"{client_without_contact.last_name} "
            + f"{client_without_contact.first_name}; No sales contact yet..."
        )

    @pytest.mark.usefixtures("client")
    def test_full_name_property(self, client):
        assert client.full_name == f"{client.last_name} {client.first_name}"


@pytest.mark.django_db
class TestClientViews:
    CLIENT_LIST_URL = reverse("clients-list")

    @pytest.mark.usefixtures("sales_user", "sales_user_authenticated_client")
    def test_sales_user_list_access(self, sales_user, sales_user_authenticated_client):
        response = sales_user_authenticated_client.get(self.CLIENT_LIST_URL)
        assert response.status_code == status.HTTP_200_OK

    @pytest.mark.usefixtures("superuser", "superuser_authenticated_client")
    def test_superuser_list_access(self, superuser, superuser_authenticated_client):
        response = superuser_authenticated_client.get(self.CLIENT_LIST_URL)
        assert response.status_code == status.HTTP_200_OK

    @pytest.mark.usefixtures("superuser", "superuser_authenticated_client")
    def test_superuser_create_access(self, superuser, superuser_authenticated_client):
        response = superuser_authenticated_client.post(self.CLIENT_LIST_URL)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.usefixtures("sales_user", "sales_user_authenticated_client")
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
