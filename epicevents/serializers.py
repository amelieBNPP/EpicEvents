from django.contrib.auth.models import User
from rest_framework.serializers import ModelSerializer

from epicevents.models import Client, Contract, Employee, Event


class EmployeeSerializer(ModelSerializer):

    class Meta:
        model = Employee
        fields = [
            'id',
            'function',
            'role',
            'employee_contact',
        ]


class ClientSerializer(ModelSerializer):

    class Meta:
        model = Client
        fields = [
            'id',
            'compagny_name',
            'status',
            'client_contact',
            'sales_contact',
        ]


class ContractSerializer(ModelSerializer):
    class Meta:
        model = Contract
        fields = [
            'id',
            'amount',
            'payment_due',
            'client_contact',
            'sales_contact',
        ]


class EventSerializer(ModelSerializer):
    class Meta:
        model = Event
        fields = [
            'id',
            'event_date',
            'notes',
            'attendees',
            'closed',
            'contract_reference',
            'support_contact',
        ]
