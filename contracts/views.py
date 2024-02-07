from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from django.http import HttpResponseNotFound

from .serializers import ContractSerializer
from .models import Contract
from .permissions import ContractPermissions


class ContractViewSet(ModelViewSet):
    """Views for CRUD operations on Contract model."""

    serializer_class = ContractSerializer
    permission_classes = [IsAuthenticated, ContractPermissions]
    queryset = Contract.objects.all()

    @action(detail=False)
    def signed_unpaid(self, request):
        if Contract.objects.filter(sales_contact=request.user).exists():
            contracts = Contract.objects.filter(
                signed=True, amount_due__gt=0.0, sales_contact=request.user
            )
            serializer = ContractSerializer(contracts, many=True)
            return Response(serializer.data)
        else:
            return HttpResponseNotFound(
                "Sorry, we couldn't find data corresponding your request."
            )

    @action(detail=False)
    def unsigned(self, request):
        if Contract.objects.filter(sales_contact=request.user).exists():
            contracts = Contract.objects.filter(
                signed=False, sales_contact=request.user
            )
            serializer = ContractSerializer(contracts, many=True)
            return Response(serializer.data)
        else:
            return HttpResponseNotFound(
                "Sorry, we couldn't find data corresponding your request."
            )

    @action(detail=False)
    def unpaid(self, request):
        if Contract.objects.filter(sales_contact=request.user).exists():
            contracts = Contract.objects.filter(
                amount_due__gt=0.0, sales_contact=request.user
            )
            serializer = ContractSerializer(contracts, many=True)
            return Response(serializer.data)
        else:
            return HttpResponseNotFound(
                "Sorry, we couldn't find data corresponding your request."
            )
