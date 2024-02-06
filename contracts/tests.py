import pytest


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
