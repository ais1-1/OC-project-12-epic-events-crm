from rest_framework import serializers
from django.contrib.auth import get_user_model

from .models import Event
from contracts.models import Contract
from teams.models import Team

User = get_user_model()


class EventSerializer(serializers.ModelSerializer):
    support_contact_name = serializers.SerializerMethodField()
    support_contact_email = serializers.SerializerMethodField()
    client_name = serializers.SerializerMethodField()
    client_contact = serializers.SerializerMethodField()

    contract = serializers.PrimaryKeyRelatedField(
        queryset=Contract.objects.filter(signed=True),
        pk_field=serializers.UUIDField(format="hex"),
    )
    support_contact = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(role=Team.get_support_team()),
        allow_null=True,
        required=False,
    )

    start_date = serializers.DateTimeField(required=True, format="%Y-%m-%d %H:%M")
    end_date = serializers.DateTimeField(required=True, format="%Y-%m-%d %H:%M")
    updated_date = serializers.DateTimeField(read_only=True, format="%Y-%m-%d")
    created_date = serializers.DateTimeField(read_only=True, format="%Y-%m-%d")

    class Meta:
        model = Event
        fields = "__all__"
        read_only__fields = [
            "created_date",
            "updated_date",
            "id",
            "support_contact_name",
            "support_contact_email",
            "client_name",
            "client_contact",
        ]

    def get_support_contact_name(self, obj):
        if obj.support_contact:
            return obj.support_contact.full_name
        else:
            return "No support team contact yet."

    def get_support_contact_email(self, obj):
        if obj.support_contact:
            return obj.support_contact.email
        else:
            return ""

    def get_client_name(self, obj):
        return obj.client_name

    def get_client_contact(self, obj):
        return f"email: {obj.client_email}\nphone: {obj.client_phone}"
