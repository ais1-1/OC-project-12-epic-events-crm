from rest_framework import serializers

from .models import Event


class EventSerializer(serializers.ModelSerializer):
    support_contact_name = serializers.SerializerMethodField()
    support_contact_email = serializers.SerializerMethodField()
    client_name = serializers.SerializerMethodField()
    client_contact = serializers.SerializerMethodField()

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
            return "The event has not yet an support team contact."

    def get_support_contact_email(self, obj):
        if obj.support_contact:
            return obj.support_contact.email
        else:
            return "The event has not yet an support team contact."

    def get_client_name(self, obj):
        return obj.client_name

    def get_client_contact(self, obj):
        return f"email: {obj.client_email}; phone: {obj.client_phone}"
