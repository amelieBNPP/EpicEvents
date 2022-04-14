from django.db import models
from django.conf import settings

ROLE = (
    ('manager', 'Manager'),
    ('sales', 'Sales'),
    ('support', 'Support'),
)


class Employee(models.Model):
    function = models.CharField(max_length=250)
    role = models.CharField(choices=ROLE, max_length=25)
    employee_contact = models.OneToOneField(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )


class Client(models.Model):
    compagny_name = models.CharField(max_length=250)
    last_contact = models.DateTimeField(auto_now=True)
    status = models.BooleanField()
    client_contact = models.OneToOneField(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    sales_contact = models.OneToOneField(
        to=Employee,
        on_delete=models.CASCADE,
    )


class Contract(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    amount = models.FloatField()
    payment_due = models.DateField()
    client_contact = models.ForeignKey(
        to=Client,
        on_delete=models.CASCADE,
    )
    sales_contact = models.ForeignKey(
        to=Employee,
        on_delete=models.CASCADE,
    )


class Event(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    event_date = models.DateField()
    notes = models.TextField(max_length=2048, blank=True)
    attendees = models.IntegerField()
    closed = models.BooleanField()
    contract_reference = models.ForeignKey(
        to=Contract,
        on_delete=models.CASCADE,
    )
    support_contact = models.ForeignKey(
        to=Employee,
        on_delete=models.CASCADE,
    )
