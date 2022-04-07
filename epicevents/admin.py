from django.contrib import admin

from .models import Employee, Client, Contract, Event

admin.site.register(Employee)
admin.site.register(Client)
admin.site.register(Contract)
admin.site.register(Event)
