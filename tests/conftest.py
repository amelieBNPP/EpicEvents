import pytest
from django.core.management import call_command


@pytest.fixture(scope='session')
def django_db_setup(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        call_command('loaddata', 'tests/mock_database.json')


@pytest.fixture
def new_client_user(django_user_model):
    username = "newclient"
    user = django_user_model.objects.get(username=username)
    return user


@pytest.fixture
def new_sales_user(django_user_model):
    username = "newsales"
    user = django_user_model.objects.get(username=username)
    return user


@pytest.fixture
def other_sales_user(django_user_model):
    username = "othersales"
    user = django_user_model.objects.get(username=username)
    return user


@pytest.fixture
def new_manager_user(django_user_model):
    username = "newmanager"
    user = django_user_model.objects.get(username=username)
    return user


@pytest.fixture
def new_support_user(django_user_model):
    username = "newsupport"
    user = django_user_model.objects.get(username=username)
    return user


@pytest.fixture
def new_sales_loggin(client, new_sales_user):
    client.force_login(new_sales_user)
    return client


@pytest.fixture
def other_sales_loggin(client, other_sales_user):
    client.force_login(other_sales_user)
    return client


@pytest.fixture
def new_manager_loggin(client, new_manager_user):
    client.force_login(new_manager_user)
    return client


@pytest.fixture
def new_support_loggin(client, new_support_user):
    client.force_login(new_support_user)
    return client
