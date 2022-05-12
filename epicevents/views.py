from datetime import datetime

from epicevents.serializers import (
    EmployeeSerializer,
    ClientSerializer,
    ContractSerializer,
    EventSerializer,
)
from epicevents.models import Client, Employee, Contract, Event
from epicevents.filters import ContractFilter, ClientFilter, EventFilter, EmployeeFilter
from epicevents.permission import ManagerPermission, SalesPermission, SupportPermission
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.core import serializers

from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.http import Http404, HttpResponse


class EmployeesViewset(ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [IsAuthenticated, ManagerPermission]

    def list(self, request):
        queryset = self.get_queryset()
        self.check_object_permissions(request, None)
        myfilter = EmployeeFilter(
            request.GET,
            queryset=queryset,
        )
        serializer = serializers.serialize("json", myfilter.qs)
        return HttpResponse(serializer, content_type="application/json")

    def create(self, request):
        """
        Create Employee.
        """
        self.check_object_permissions(request, None)
        request_data = request.data.copy()
        user = get_object_or_404(
            User,
            username=request.data['employee_contact'],
        )
        employee = Employee.objects.filter(
            employee_contact=user.pk,
        )

        if employee:
            return Response(
                data="Employee already exists.",
                status=status.HTTP_409_CONFLICT,
            )

        serializer = EmployeeSerializer(data=request.data)

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


class ClientsViewset(ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticated, SalesPermission]

    def list(self, request):
        queryset = self.get_queryset()
        self.check_object_permissions(request, None)
        myfilter = ClientFilter(
            request.GET,
            queryset=queryset,
        )
        serializer = serializers.serialize("json", myfilter.qs)
        return HttpResponse(serializer, content_type="application/json")

    def create(self, request):
        """
        Create Client.
        """
        request_data = request.data.copy()
        employee = get_object_or_404(
            Employee,
            employee_contact=self.request.user.id,
        )
        self.check_object_permissions(request, employee)
        try:
            user = User.objects.get(
                username=request.data['client_contact'],
            )
        except:
            return Response(
                data="User does not exists.",
                status=status.HTTP_404_NOT_FOUND,
            )
        
        client = Client.objects.filter(client_contact=user.pk)
        if client:
            return Response(
                data="Client already exists.",
                status=status.HTTP_409_CONFLICT,
            )


        request_data.update(
            {
                'sales_contact': employee.id,
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
    permission_classes = [IsAuthenticated, SalesPermission]
    filterset_class = ContractFilter

    def list(self, request, client_pk=None):
        queryset = self.get_queryset()
        self.check_object_permissions(request, None)
        if client_pk is not None:
            queryset = Contract.objects.filter(
                client_contact=client_pk,
            )
        myfilter = ContractFilter(
            request.GET,
            queryset=queryset,
        )
        serializer = serializers.serialize("json", myfilter.qs)
        return HttpResponse(serializer, content_type="application/json")

    def create(self, request, client_pk=None):
        """Create project if permission and add the owner as contributor."""
        request_data = request.data.copy()
        self.check_object_permissions(request, None)
        employee = get_object_or_404(
            Employee,
            employee_contact=self.request.user.id,
        )

        try:
            client = Client.objects.get(
                pk=client_pk,
            )
        except:
            return Response(
                data="Client does not exists.",
                status=status.HTTP_404_NOT_FOUND,
            )

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
    permission_classes = [IsAuthenticated, SupportPermission]

    def list(self, request, client_pk=None, contract_pk=None):
        queryset = self.get_queryset()
        self.check_object_permissions(request, None)
        if contract_pk and client_pk:
            contract = Contract.objects.get(
                pk=contract_pk
            )
            if client_pk == contract.id:
                quesryset = Event.objects.filter(
                    contract_reference_id=contract_pk,
                )

        myfilter = EventFilter(
            request.GET,
            queryset=queryset,
        )
        serializer = serializers.serialize("json", myfilter.qs)
        return HttpResponse(serializer, content_type="application/json")

    def create(self, request, client_pk=None, contract_pk=None):
        """Create project if permission and add the owner as contributor."""
        request_data = request.data.copy()
        try:
            contract = Contract.objects.get(
                pk=contract_pk,
            )
        except:
            return Response(
                data="Contract does not exists.",
                status=status.HTTP_404_NOT_FOUND,
            )

        try:
            Client.objects.get(pk=client_pk)
        except:
            return Response(
                data="Client does not exists.",
                status=status.HTTP_404_NOT_FOUND,
            )
        
        is_event = Event.objects.filter(contract_reference=contract_pk)
        if is_event:
            return Response(
                data="Event already exists.",
                status=status.HTTP_409_CONFLICT,
            )
            
        self.check_object_permissions(request, contract)
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

    def update(self, request, client_pk=None, contract_pk=None, pk=None):
        """Update project until the event is open and if permission"""
        request_data = request.data.copy()
        self.check_object_permissions(request, None)
        try:
            event = Event.objects.get(pk=pk)
        except:
            return Response(
                data="Event does not exists.",
                status=status.HTTP_404_NOT_FOUND,
            )
        if datetime(event.event_date.year, event.event_date.month, event.event_date.day) < datetime.now():
            return Response(
                data="Event already past.",
                status=status.HTTP_409_CONFLICT,
            )
        try:
            contract = Contract.objects.get(
                pk=contract_pk,
            )
        except:
            return Response(
                data="Contract does not exists.",
                status=status.HTTP_404_NOT_FOUND,
            )
        try:
            Client.objects.get(pk=client_pk)
        except:
            return Response(
                data="Client does not exists.",
                status=status.HTTP_404_NOT_FOUND,
            )

        request_data.update(
            {
                'closed': request.data['closed'],
                'attendees': request.data['attendees'],
                'event_date': request.data['event_date'],
                'notes': request.data['notes'],
                'support_contact':request.data['support_contact'],
            }
        )
        serializer = EventSerializer(event, data=request_data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                data=serializer.data,
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
