import json


def test_get_emplyee_filter(new_manager_loggin):
    client = new_manager_loggin
    response = client.get(
        path='/epicevents/employees/?sort_by=-role',
    )
    response_data = json.loads(response.content.decode("utf-8"))
    list_role = list()
    for data in response_data:
        data_fields = data["fields"]
        list_role.append(data_fields["role"])
    assert list_role == ['support', 'sales', 'sales', 'manager']
    assert response.status_code == 200


def test_get_client_filter(new_sales_loggin):
    client = new_sales_loggin
    response = client.get(
        path='/epicevents/clients/?compagny_name=newCompagnie',
    )
    response_data = json.loads(response.content.decode("utf-8"))
    assert len(response_data) == 1
    for data in response_data:
        data_fields = data["fields"]
        assert data_fields["compagny_name"] == "newCompagnie"
    assert response.status_code == 200


def test_get_contract_filter(new_sales_loggin):
    client = new_sales_loggin
    response = client.get(
        path='/epicevents/clients/1/contracts/?min_amount=1000&max_amount=10000',
    )
    response_data = json.loads(response.content.decode("utf-8"))
    for data in response_data:
        data_fields = data["fields"]
        assert data_fields["amount"] < 10000
        assert data_fields["amount"] > 1000
    assert response.status_code == 200


def test_get_event_filter(new_sales_loggin):
    client = new_sales_loggin
    response = client.get(
        path='/epicevents/events/?min_attendees=100&max_attendees=500',
    )
    response_data = json.loads(response.content.decode("utf-8"))
    for data in response_data:
        data_fields = data["fields"]
        assert data_fields["attendees"] > 100
        assert data_fields["attendees"] < 500
    assert response.status_code == 200
