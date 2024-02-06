import pytest


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
