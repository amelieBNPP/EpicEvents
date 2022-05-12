from rest_framework.permissions import BasePermission
from .models import Employee, Client, Event


class ManagerPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        try:
            employee = Employee.objects.get(employee_contact=request.user)
        except Employee.DoesNotExist:
            return False
        if request.method == 'GET':
            return True
        return employee.role == 'manager'


class SalesPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        """
        For safe methode (GET) => return permission
        Otherwise if the employee is in charge of the client => return permission
        Otherwise => no permission is given
        """
        if request.method == 'GET':
            return True
        try:
            employee = Employee.objects.get(employee_contact=request.user)
        except Employee.DoesNotExist:
            return False
        if employee.role == 'manager':
            return True
        if employee.role == 'sales':
            if obj:
                return True
            else:
                client = Client.objects.get(
                    pk=view.kwargs['client_pk'],
                )
                return client.sales_contact.id == employee.id
        return False


class SupportPermission(BasePermission):

    def has_object_permission(self, request, view, obj):
        """
        For safe methode (GET) => return permission
        Otherwise if the employee is in charge of the event => return permission
        Otherwise => no permission is given
        """
        if request.method == 'GET':
            return True

        try:
            employee = Employee.objects.get(employee_contact=request.user)
        except Employee.DoesNotExist:
            return False

        if employee.role == 'manager':
            return True
        if employee.role == 'sales':
            client = Client.objects.get(
                pk=view.kwargs['client_pk'],
            )
            return client.sales_contact.id == employee.id
        if employee.role == 'support':
            if obj:
                return False
            else:
                event = Event.objects.get(
                    contract_reference=view.kwargs['pk'],
                )
            return event.support_contact.id == employee.id
        return False
