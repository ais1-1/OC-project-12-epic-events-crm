from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from django.http import HttpResponseNotFound
from rest_framework import status

from .serializers import ContractSerializer
from .models import Contract
from .permissions import ContractPermissions


class ContractViewSet(ModelViewSet):
    """Views for CRUD operations on Contract model.

    Methods:
    own (action) - show contracts list if the authenticated user is the sales contact
    unsigned (action) -  show unsigned contracts
    unpaid (action) - show unpaid contracts
    signed (action) - show signed contracts
    without_event (action) - show contracts that do not have an event
    """

    serializer_class = ContractSerializer
    permission_classes = [IsAuthenticated, ContractPermissions]
    queryset = Contract.objects.all()

    @action(detail=False)
    def own(self, request):
        if Contract.objects.filter(sales_contact=request.user).count() > 0:
            contracts = Contract.objects.filter(sales_contact=request.user)
            serializer = ContractSerializer(contracts, many=True)
            return Response(serializer.data)
        else:
            return HttpResponseNotFound(
                "Sorry, we couldn't find data corresponding your request."
            )

    @action(detail=False)
    def unsigned(self, request):
        if Contract.objects.all().count() > 0:
            contracts = Contract.objects.filter(signed=False)
            serializer = ContractSerializer(contracts, many=True)
            return Response(serializer.data)
        else:
            return HttpResponseNotFound(
                "Sorry, we couldn't find data corresponding your request."
            )

    @action(detail=False)
    def unpaid(self, request):
        if Contract.objects.all().count() > 0:
            contracts = Contract.objects.filter(amount_due__gt=0.0)
            serializer = ContractSerializer(contracts, many=True)
            return Response(serializer.data)
        else:
            return HttpResponseNotFound(
                "Sorry, we couldn't find data corresponding your request."
            )

    @action(detail=False)
    def signed(self, request):
        if Contract.objects.all().count() > 0:
            contracts = Contract.objects.filter(signed=True)
            serializer = ContractSerializer(contracts, many=True)
            return Response(serializer.data)
        else:
            return HttpResponseNotFound(
                "Sorry, we couldn't find data corresponding your request."
            )

    @action(detail=False)
    def without_event(self, request):
        contracts = Contract.objects.filter(signed=True).filter(event__isnull=True)
        if contracts.count() > 0:
            serializer = ContractSerializer(contracts, many=True)
            return Response(serializer.data)
        elif contracts.count() == 0:
            response = {
                "status": status.HTTP_204_NO_CONTENT,
                "message": "All the signed contracts have associated events.",
            }
            return Response(response, status=status.HTTP_204_NO_CONTENT)
