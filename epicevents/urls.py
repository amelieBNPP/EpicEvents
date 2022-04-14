from django.urls import path

from . import views

from rest_framework import routers
from rest_framework_nested import routers
from epicevents.views import (
    EmployeesViewset,
    ClientsViewset,
    ContractsViewset,
    EventsViewset,
)
from django.urls import path, include

# Ici nous créons notre routeur
router = routers.SimpleRouter()
router.register('employees', EmployeesViewset, basename='employees')
router.register('clients', ClientsViewset, basename='clients')
router.register('contracts', ContractsViewset, basename='contracts')
router.register('events', EventsViewset, basename='events')

client_router = routers.NestedSimpleRouter(
    router,
    r'clients',
    lookup='client',
)
client_router.register(r'contracts', ContractsViewset, basename='contracts')

contract_router = routers.NestedSimpleRouter(
    client_router,
    r'contracts',
    lookup='contract',
)
contract_router.register(r'events', EventsViewset, basename='events')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(client_router.urls)),
    path('', include(contract_router.urls)),
    path('', views.index, name='index'),
]
