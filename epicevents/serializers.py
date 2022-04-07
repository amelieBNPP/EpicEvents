from django.contrib.auth.models import User
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from epicevents.models import Client


class ClientSerializer(ModelSerializer):
    client_contact = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field='username',
    )

    class Meta:
        model = Client
        fields = [
            'id',
            'compagny_name',
            'status',
            'client_contact',
        ]

    def validate_project(self, value):
        if Client.objects.filter(client_contact=value).exists():
            raise serializers.ValidationError('Client already exists')
        return value
