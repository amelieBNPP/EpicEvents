from django.contrib import admin

from .models import Person, Employee, Client, Contract, Event

admin.site.register(Person)
admin.site.register(Employee)
admin.site.register(Client)
admin.site.register(Contract)
admin.site.register(Event)
