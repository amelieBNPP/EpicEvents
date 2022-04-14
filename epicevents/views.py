from epicevents.serializers import (
    EmployeeSerializer,
    ClientSerializer,
    ContractSerializer,
    EventSerializer,
)
from epicevents.models import Client, Employee, Contract, Event
from epicevents.permission import EventPermission, ClientPermission, EmployeePermission
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.http import JsonResponse

from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.http import HttpResponse


class EmployeesViewset(ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [IsAuthenticated, EmployeePermission]


class ClientsViewset(ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticated, ClientPermission]

    def create(self, request):
        """
        Create Client.
        """
        request_data = request.data.copy()
        employee = get_object_or_404(
            Employee,
            employee_contact=self.request.user.id,
        )
        try:
            client = get_object_or_404(
                User,
                pk=request.data['client_contact'],
            )
        except:
            return HttpResponse("Client user does not exists.")

        request_data.update(
            {
                'sales_contact': employee.id,
                'client_contact': client.id,
            }
        )

        serializer = ClientSerializer(data=request_data)

        if serializer.is_valid():

            serializer.save()
            return Response(
                data=serializer.data,
                status=status.HTTP_201_CREATED,
            )
        return Response(
            data=serializer.data,
            status=status.HTTP_400_BAD_REQUEST,
        )


class ContractsViewset(ModelViewSet):
    queryset = Contract.objects.all()
    serializer_class = ContractSerializer
    permission_classes = [IsAuthenticated, ClientPermission]

    def create(self, request, client_pk=None):
        """Create project if permission and add the owner as contributor."""
        request_data = request.data.copy()

        employee = get_object_or_404(
            Employee,
            employee_contact=self.request.user.id,
        )

        try:
            client = Client.objects.get(
                pk=client_pk,
            )
        except:
            return HttpResponse("Client does not exists.")

        request_data.update(
            {
                'sales_contact': employee.id,
                'client_contact': client.id,
            }
        )

        serializer = ContractSerializer(data=request_data)
        if serializer.is_valid():
            serializer.save()
            client.status = True
            client.save()
            return Response(
                data=serializer.data,
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EventsViewset(ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated, EventPermission]

    def create(self, request, client_pk=None, contract_pk=None):
        """Create project if permission and add the owner as contributor."""
        request_data = request.data.copy()

        try:
            contract = Contract.objects.get(
                pk=contract_pk,
            )
        except:
            return HttpResponse("Contract does not exists.")

        try:
            Client.objects.get(pk=client_pk)
        except:
            return HttpResponse("Client does not exists.")

        request_data.update(
            {
                'closed': False,
                'contract_reference': contract.id,
            }
        )
        serializer = EventSerializer(data=request_data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                data=serializer.data,
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
