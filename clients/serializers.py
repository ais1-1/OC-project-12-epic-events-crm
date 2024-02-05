from rest_framework import serializers
from .models import Client


class ClientSerializer(serializers.ModelSerializer):

    sales_contact_name = serializers.SerializerMethodField()
    sales_contact_email = serializers.SerializerMethodField()

    class Meta:
        model = Client
        fields = "__all__"
        read_only__fields = [
            "created_date",
            "updated_date",
            "sales_contact",
            "id",
            "sales_contact_name",
            "sales_contact_email",
        ]

    def get_sales_contact_name(self, obj):
        if obj.sales_contact:
            return obj.sales_contact.full_name
        else:
            return "The client has no contact added from Sales team."

    def get_sales_contact_email(self, obj):
        if obj.sales_contact:
            return obj.sales_contact.email
        else:
            return "The client has no contact added from Sales team."
