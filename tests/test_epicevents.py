from epicevents.models import Client, Contract, Employee, Event


def test_create_employee(new_manager_loggin):
    client = new_manager_loggin
    nb_employees = Employee.objects.count()
    response = client.post(
        path='/epicevents/employees/',
        data={
            "function": "support",
            "role": "support",
            "employee_contact": 2
        },
    )
    assert Employee.objects.count() == nb_employees + 1
    assert response.status_code == 201


def test_create_client(new_sales_loggin):
    client = new_sales_loggin
    nb_clients = Client.objects.count()
    response = client.post(
        path='/epicevents/clients/',
        data={
            'compagny_name': 'new_compagny',
            'status': False,
            'client_contact': 4,
        },
    )
    assert Client.objects.count() == nb_clients + 1
    assert response.status_code == 201


def test_create_contract(new_sales_loggin):
    client = new_sales_loggin
    nb_contracts = Contract.objects.count()
    response = client.post(
        path='/epicevents/clients/1/contracts/',
        data={
            "amount": 5000,
            "payment_due": "2022-07-21",
        },
    )
    assert Contract.objects.count() == nb_contracts + 1
    assert response.status_code == 201


def test_create_event(new_sales_loggin):
    client = new_sales_loggin
    nb_events = Event.objects.count()
    response = client.post(
        path='/epicevents/clients/1/contracts/1/events/',
        data={
            "attendees": 350,
            "event_date": "2022-06-30",
            "notes": "soirée de gala avec très hautes prestations",
            "support_contact": 2
        },
    )
    assert Event.objects.count() == nb_events + 1
    assert response.status_code == 201
