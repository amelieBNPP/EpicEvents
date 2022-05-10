from django.contrib.auth.models import User
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from epicevents.models import Client, Contract, Employee, Event


class EmployeeSerializer(ModelSerializer):

    employee_contact = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field='username',
    )

    class Meta:
        model = Employee
        fields = [
            'id',
            'function',
            'role',
            'employee_contact',
        ]


class ClientSerializer(ModelSerializer):
    client_contact = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field='username',
    )
    sales_contact = serializers.SlugRelatedField(
        queryset=Employee.objects.all(),
        slug_field='id',
    )
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

    client_contact = serializers.SlugRelatedField(
        queryset=Client.objects.all(),
        slug_field='id',
    )
    sales_contact = serializers.SlugRelatedField(
        queryset=Employee.objects.all(),
        slug_field='id',
    )

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

    contract_reference = serializers.SlugRelatedField(
        queryset=Contract.objects.all(),
        slug_field='id',
    )        
    support_contact = serializers.SlugRelatedField(
        queryset=Employee.objects.all(),
        slug_field='id',
    )

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
