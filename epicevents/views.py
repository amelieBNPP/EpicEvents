from epicevents.serializers import (
    EmployeeSerializer,
    ClientSerializer,
    ContractSerializer,
    EventSerializer,
)
from epicevents.models import Client, Employee, Contract, Event
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, world. You're at the EpicEvents index.")


class EmployeesViewset(ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [IsAuthenticated]


class ClientsViewset(ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request):
        """
        Create Client.
        """
        request_data = request.data.copy()
        try:
            employee = get_object_or_404(
                Employee,
                employee_contact=self.request.user.id,
            )
        except:
            return HttpResponse("Your are not regiter as employee. Permission denied.")

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
    permission_classes = [IsAuthenticated]

    def list(self, request, client_pk=None):
        """ GET all contracts if permission"""
        clients = get_object_or_404(Client, pk=client_pk)
        contracts = get_object_or_404(Contract, client_contact=clients.id)
        queryset = Contract.objects.filter(client_contact=client_pk)
        serializer = ContractSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, client_pk=None):
        """Create project if permission and add the owner as contributor."""
        request_data = request.data.copy()
        try:
            employee = get_object_or_404(
                Employee,
                employee_contact=self.request.user.id,
            )
        except:
            return HttpResponse("Your are not regiter as employee. Permission denied.")

        try:
            client = get_object_or_404(
                Client,
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
    permission_classes = [IsAuthenticated]

    def create(self, request, client_pk=None, contract_pk=None):
        """Create project if permission and add the owner as contributor."""
        request_data = request.data.copy()
        try:
            employee = get_object_or_404(
                Employee,
                employee_contact=self.request.user.id,
            )
        except:
            return HttpResponse("Your are not regiter as employee. Permission denied.")

        try:
            print(request.data)
            employee = get_object_or_404(
                Employee,
                pk=request.data['support_contact'],
            )
        except:
            return HttpResponse("The support employee does not exist.")

        try:
            contract = get_object_or_404(
                Contract,
                pk=contract_pk,
            )
        except:
            return HttpResponse("Contract does not exists.")

        try:
            client = get_object_or_404(
                Client,
                pk=client_pk,
            )
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
