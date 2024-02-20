from rest_framework import serializers

from .models import Contract


class ContractSerializer(serializers.ModelSerializer):
    """Serializes Contract model"""

    sales_contact_name = serializers.SerializerMethodField()
    sales_contact_email = serializers.SerializerMethodField()
    client_name = serializers.SerializerMethodField()
    client_email = serializers.SerializerMethodField()

    updated_date = serializers.DateTimeField(read_only=True, format="%Y-%m-%d")
    created_date = serializers.DateTimeField(read_only=True, format="%Y-%m-%d")

    class Meta:
        model = Contract
        fields = "__all__"
        read_only__fields = [
            "created_date",
            "updated_date",
            "id",
            "sales_contact_name",
            "sales_contact_email",
            "client_name",
            "client_email",
        ]

    def get_sales_contact_name(self, obj):
        if obj.sales_contact:
            return obj.sales_contact.full_name
        else:
            return "The contract has no contact added from Sales team."

    def get_sales_contact_email(self, obj):
        if obj.sales_contact:
            return obj.sales_contact.email
        else:
            return "The contract has no contact added from Sales team."

    def get_client_name(self, obj):
        if obj.client:
            return obj.client.full_name
        else:
            return "The contract is not connected to a client."

    def get_client_email(self, obj):
        if obj.client:
            return obj.client.email
        else:
            return "The contract is not connected to a client."
