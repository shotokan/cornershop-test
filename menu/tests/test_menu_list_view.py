from typing import List

import pytest
from django.contrib.auth.models import User
from pytest_django.asserts import assertTemplateUsed


@pytest.fixture
def user_test(db, django_user_model) -> User:
    username = "user1"
    password = "bar"
    user = django_user_model.objects.create_user(username=username, password=password)
    return user


def test_should_fail_trying_to_get_the_form_to_list_menus_as_staff(client, user_test):
    client.force_login(user_test)
    client.login(username=user_test.username, password=user_test.password)
    response = client.get("/menu/list", follow=True)

    assert response.status_code == 403


def test_should_get_the_form_to_list_menus_as_admin(client, admin_user):
    client.force_login(admin_user)
    client.login(username=admin_user.username, password=admin_user.password)
    response = client.get("/menu/list", follow=True)
    html = response.content.decode("utf8")

    assert "Menu List" in html
    assert response.status_code == 200
