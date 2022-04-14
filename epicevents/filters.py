import django_filters
from epicevents.models import Contract, Event, Client, Employee


class EmployeeFilter(django_filters.FilterSet):

    role = django_filters.CharFilter(
        field_name="role",
        lookup_expr='iexact',
    )

    sort_by = django_filters.CharFilter(
        method='my_custom_filter',
        label="Sort by a given value (role, -role, etc.)",
    )

    def my_custom_filter(self, queryset, name, value):
        values = value.lower().split(',')
        return queryset.order_by(*values)

    class Meta:
        model = Employee
        fields = [
            'id',
            'function',
            'role',
            'employee_contact',
        ]


class ClientFilter(django_filters.FilterSet):

    sort_by = django_filters.CharFilter(
        method='my_custom_filter',
        label="Sort by a given value (compane_name, -company_name, etc.)",
    )

    def my_custom_filter(self, queryset, name, value):
        values = value.lower().split(',')
        return queryset.order_by(*values)

    class Meta:
        model = Client
        fields = [
            'id',
            'compagny_name',
            'status',
            'client_contact',
            'sales_contact',
        ]


class ContractFilter(django_filters.FilterSet):

    min_amount = django_filters.NumberFilter(
        field_name="amount",
        lookup_expr='gte',
    )
    max_amount = django_filters.NumberFilter(
        field_name="amount",
        lookup_expr='lte',
    )

    sort_by = django_filters.CharFilter(
        method='my_custom_filter',
        label="Sort by a given value (amount, -amount, etc.)",
    )

    def my_custom_filter(self, queryset, name, value):
        values = value.lower().split(',')
        return queryset.order_by(*values)

    class Meta:
        model = Contract
        fields = [
            'id',
            'amount',
            'payment_due',
            'client_contact',
            'sales_contact',
        ]


class EventFilter(django_filters.FilterSet):

    min_attendees = django_filters.NumberFilter(
        field_name="attendees",
        lookup_expr='gte',
    )
    max_attendees = django_filters.NumberFilter(
        field_name="attendees",
        lookup_expr='lte',
    )

    sort_by = django_filters.CharFilter(
        method='my_custom_filter',
        label="Sort by a given value (event_date, -event_date, etc.)",
    )

    def my_custom_filter(self, queryset, name, value):
        values = value.lower().split(',')
        return queryset.order_by(*values)

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
