
def test_get_employee_permission(new_support_loggin):
    client = new_support_loggin
    response = client.delete(
        path='/epicevents/employees/1/',
    )
    assert response.status_code == 403


def test_get_client_permission(new_support_loggin):
    client = new_support_loggin
    response = client.delete(
        path='/epicevents/clients/1/',
    )
    assert response.status_code == 403


def test_get_contract_permission(other_sales_loggin):
    client = other_sales_loggin
    response = client.put(
        path='/epicevents/clients/1/contracts/1/',
        data={
            "amount": 5005,
            "payment_due": "2022-07-23",
        },
    )
    assert response.status_code == 403


def test_get_event_permission(other_sales_loggin):
    client = other_sales_loggin
    response = client.delete(
        path='/epicevents/clients/1/contracts/1/events/1/',
    )
    assert response.status_code == 403
