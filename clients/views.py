from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from django.db import transaction

from .serializers import ClientSerializer
from .models import Client
from .permissions import ClientPermissions


class ClientViewSet(ModelViewSet):
    """Views for CRUD operations on Client model."""

    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticated, ClientPermissions]
    queryset = Client.objects.all()

    @transaction.atomic
    def perform_create(self, serializer):
        """Assign the user as sales contact"""
        serializer.save(sales_contact=self.request.user)
