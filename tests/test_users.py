import pytest
from django.contrib.auth.models import User


@pytest.mark.django_db
def test_signup(client):
    nb_user = User.objects.count()
    response = client.post(
        path='/user/signup/',
        data={
            "username": "test_user_client",
            "email": "test_user_client@gmail.com",
            "first_name": "user",
            "last_name": "client",
            "password": "Password12345"
        }
    )
    new_nb_user = User.objects.count()
    assert new_nb_user == (nb_user + 1)
    assert response.status_code == 201
