from django.contrib.auth.models import User
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from epicevents.models import Client, Contract, Employee, Event


class EmployeeSerializer(ModelSerializer):

    employee_contact = serializers.StringRelatedField()

    class Meta:
        model = Employee
        fields = [
            'id',
            'function',
            'role',
            'employee_contact',
        ]


class ClientSerializer(ModelSerializer):
    client_contact = serializers.StringRelatedField()
    sales_contact = serializers.StringRelatedField()

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

    client_contact = serializers.StringRelatedField()
    sales_contact = serializers.StringRelatedField()

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

    contract_reference = serializers.StringRelatedField()
    support_contact = serializers.StringRelatedField()

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
