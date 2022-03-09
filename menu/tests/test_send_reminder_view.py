from unittest import mock
import uuid
from typing import List

import pytest
from django.contrib.auth.models import User
from django.utils import timezone

from menu.models import Menu, MenuItem
from share.notification.tasks import send_menu_notification


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


def test_should_send_reminder_as_admin(client, admin_user, today_menu_test):
    client.force_login(admin_user)
    client.login(username=admin_user.username, password=admin_user.password)
    with mock.patch("share.notification.tasks.send_menu_notification.delay") as delay:
        response = client.get("/menu/reminder", follow=True)

        delay.assert_called_once()
        assert response.status_code == 200


def test_should_fail_and_redirect_to_login_when_user_is_staff(
    client, user_test, today_menu_test
):
    client.force_login(user_test)
    client.login(username=user_test.username, password=user_test.password)
    with mock.patch(
        "share.notification.tasks.send_menu_notification"
    ) as send_menu_notification:
        response = client.get("/menu/reminder/", follow=True)
        last_url, status_code = response.redirect_chain[-1]

        assert status_code == 302
        assert last_url == "/account/login/?next=/menu/reminder/"
