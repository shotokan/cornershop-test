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


def test_should_fail_trying_to_get_the_form_to_update_a_menu(
    client, user_test, today_menu_test
):
    client.force_login(user_test)
    client.login(username=user_test.username, password=user_test.password)
    response = client.get(
        f"/menu/{today_menu_test.id}/update",
    )
    assert response.status_code == 403


def test_should_get_the_form_to_update_a_menu(client, admin_user, today_menu_test):
    client.force_login(admin_user)
    response = client.get(
        f"/menu/{today_menu_test.id}/update",
    )
    assert response.status_code == 200


@pytest.mark.django_db
def test_should_update_an_item_menu_admin_user(client, admin_user, today_menu_test):
    description_updated_msg = "this is updated"
    current_date = timezone.now()
    client.force_login(admin_user)
    client.login(username=admin_user.username, password=admin_user.password)
    client.post(
        f"/menu/{today_menu_test.id}/update",
        {
            "date_month": current_date.month,
            "date_day": current_date.day,
            "date_year": current_date.year,
            "has_items-TOTAL_FORMS": 4,
            "has_items-INITIAL_FORMS": 0,
            "has_items-MIN_NUM_FORMS": 0,
            "has_items-MAX_NUM_FORMS": 1000,
            "has_items-0-id": "",
            "has_items-0-menu": "",
            "has_items-0-description": description_updated_msg,
            "has_items-1-id": "",
            "has_items-1-menu": "",
            "has_items-1-description": "example2",
            "has_items-2-id": "",
            "has_items-2-menu": "",
            "has_items-2-description": "example3",
            "has_items-3-id": "",
            "has_items-3-menu": "",
            "has_items-3-description": "example4",
            "submit": "save",
        },
    )
    today_menu = Menu.objects.all()
    items = MenuItem.objects.all()
    assert len(today_menu) == 1
    assert len(items) == 4
    assert items[0].description == description_updated_msg
