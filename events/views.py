from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from django.http import HttpResponseNotFound
from rest_framework import status
from django.db import transaction

from .serializers import EventSerializer
from .models import Event
from .permissions import EventPermissions
from teams.models import Team
from contracts.models import Contract


class EventViewSet(ModelViewSet):
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated, EventPermissions]
    queryset = Event.objects.all()

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        """
        Create event if the request is from contracts sales contact and if the contract is signed.
        """
        if request.data:
            contract_id = request.data["contract"]
            contract = Contract.objects.get(id=contract_id)
            sales_contact = contract.sales_contact
            if sales_contact == request.user and contract.signed:
                serializer = self.get_serializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                self.perform_create(serializer)
                headers = self.get_success_headers(serializer.data)
                return Response(
                    serializer.data, status=status.HTTP_201_CREATED, headers=headers
                )
            else:
                message = ""
                if not contract.signed:
                    message = "Please note that you can create an event only for signed contracts."
                elif sales_contact != request.user:
                    message = (
                        "Make sure that you are creating the event for your client."
                    )

                response = {
                    "status": status.HTTP_401_UNAUTHORIZED,
                    "message": message,
                }
                return Response(response, status=status.HTTP_401_UNAUTHORIZED)

        response = {
            "status": status.HTTP_403_FORBIDDEN,
            "message": "You don't have permission to do this.",
        }
        return Response(response, status=status.HTTP_403_FORBIDDEN)

    @action(detail=False)
    def without_support(self, request):
        if Event.objects.filter(support_contact__isnull=True).count() > 0:
            events = Event.objects.filter(support_contact__isnull=True)
            serializer = EventSerializer(events, many=True)
            return Response(serializer.data)
        else:
            return HttpResponseNotFound(
                "Sorry, we couldn't find data corresponding your request."
            )

    @action(detail=False)
    def my_events(self, request):
        if (
            request.user.role == Team.get_support_team()
            and Event.objects.filter(support_contact=request.user).count() > 0
        ):
            events = Event.objects.filter(support_contact=request.user)
            serializer = EventSerializer(events, many=True)
            return Response(serializer.data)
        else:
            return HttpResponseNotFound(
                "Sorry, we couldn't find data corresponding your request."
            )
