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

    def __str__(self):
        return f"{self.employee_contact.username}, role: {self.role} \n"


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

    def __str__(self):
        return f"{self.compagny_name}: contact: {self.client_contact.username}, is_client: {self.status}, last_update: {self.last_contact} \n"


class Contract(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    contract_name = models.CharField(max_length=250, default="contract")
    signed = models.BooleanField(default=False)
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

    def __str__(self):
        return f"Contrat: {self.contract_name}, amount: {self.amount}, signed: {self.signed}, client_contract: {self.client_contact.compagny_name} \n"


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

    def __str__(self):
        return f"Event: {self.contract_reference.contract_name} \n"
