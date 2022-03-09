from typing import List
import uuid

import pytest
from django.contrib.auth.models import User
from django.utils import timezone

from menu.models import Menu, MenuItem


@pytest.fixture
def user_test(db, django_user_model) -> User:
    username = "user1"
    password = "bar"
    user = django_user_model.objects.create_user(username=username, password=password)
    return user


@pytest.fixture
def today_menu_test(user_test: User) -> Menu:
    today_menu = Menu()
    today_menu.uuid = uuid.uuid4()
    today_menu.date = timezone.now()
    today_menu.created_by = user_test
    today_menu.save()
    return today_menu


@pytest.fixture
def menu_items(db, today_menu_test) -> List[MenuItem]:
    descriptions = [
        "Corn pie, Salad and Dessert",
        "Chicken Nugget Rice, Salad and Dessert",
        "Rice with hamburger, Salad and Dessert",
        "Mushroom Salad",
    ]
    menu_items = []
    for description in descriptions:
        item = MenuItem()
        item.menu = today_menu_test
        item.description = description
        item.save()
        menu_items.append(item)
    return menu_items


def test_should_get_the_form_of_requested_orders_as_admin(
    client, admin_user, menu_items
):
    description_to_verify = "Corn pie, Salad and Dessert"
    client.force_login(admin_user)
    client.login(username=admin_user.username, password=admin_user.password)
    response = client.get("/menu/list", follow=True)
    html = response.content.decode("utf8")

    assert description_to_verify in html
    assert response.status_code == 200


def test_should_fail_trying_to_get_the_form_to_list_orders_requested_as_staff(
    client, user_test
):
    client.force_login(user_test)
    client.login(username=user_test.username, password=user_test.password)
    response = client.get("/menu/list", follow=True)

    assert response.status_code == 403
