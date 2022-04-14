from rest_framework.permissions import BasePermission, SAFE_METHODS
from .models import Employee, Client, Event


class EmployeePermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        try:
            employee = Employee.objects.get(employee_contact=request.user)
        except:
            return False
        return employee.role == 'manager'


class ClientPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        """
        For safe methode (GET) => return permission
        Otherwise if the employee is in charge of the client => return permission
        Otherwise => no permission is given
        """
        if request.method in SAFE_METHODS:
            return True
        try:
            employee = Employee.objects.get(employee_contact=request.user)
        except:
            return False
        if employee.role == 'manager':
            return True
        if employee.role == 'sales':
            client = Client.objects.get(
                pk=view.kwargs['client_pk'],
            )
            return client.sales_contact.id == employee.id
        return False


class EventPermission(BasePermission):

    def has_object_permission(self, request, view, obj):
        """
        For safe methode (GET) => return permission
        Otherwise if the employee is in charge of the event => return permission
        Otherwise => no permission is given
        """
        if request.method in SAFE_METHODS:
            return True

        try:
            employee = Employee.objects.get(employee_contact=request.user)
        except:
            return False

        if employee.role == 'manager':
            return True
        if employee.role == 'sales':
            client = Client.objects.get(
                pk=view.kwargs['client_pk'],
            )
            return client.sales_contact.id == employee.id
        if employee.role == 'support':
            event = Event.objects.get(
                pk=view.kwargs['pk'],
            )
            return event.support_contact.id == employee.id
        return False
