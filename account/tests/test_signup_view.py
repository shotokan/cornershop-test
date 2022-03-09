import pytest

from django.contrib.auth.models import User

def test_should_get_the_signup_form(client):
    response = client.get("/account/signup")
    assert response.status_code == 301

@pytest.mark.django_db
def test_should_update_an_item_menu_admin_user(client):
    username = "asdasd"
    client.post(
        f"/account/signup/",
        {
            "username": "asdasd",
            "password1": "1236978Isc",
            "password2": "1236978Isc",
        },
    )
    user = User.objects.get(username=username)
    assert user.username == username