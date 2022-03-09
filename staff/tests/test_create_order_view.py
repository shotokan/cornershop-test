from typing import List
from unittest import mock
import uuid
from django import forms

import pytest
from django.contrib.auth.models import User
from django.utils import timezone

from menu.models import Menu, MenuItem
from staff.models import Order


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


def test_should_get_the_form_to_create_order_as_admin(
    client, admin_user, today_menu_test, menu_items
):
    client.force_login(admin_user)
    response = client.get(
        f"/staff/menu/{today_menu_test.uuid}",
    )
    assert response.status_code == 200

def test_should_get_the_form_to_create_order_as_staff(
    client, user_test, today_menu_test, menu_items
):
    client.force_login(user_test)
    response = client.get(
        f"/staff/menu/{today_menu_test.uuid}",
    )
    assert response.status_code == 200


@pytest.mark.django_db
def test_should_not_create_a_new_order_when_validations_are_passed(client, admin_user, today_menu_test, menu_items):
    client.force_login(admin_user)
    client.login(username=admin_user.username, password=admin_user.password)
    with mock.patch("staff.forms.OrderForm") as OrderForm:
      OrderForm.return_value.time_validation.return_value = None
      OrderForm.return_value.unique_selection_validation.return_value = None
      response = client.post(
          f"/staff/menu/{today_menu_test.uuid}",
          {
            "menu": today_menu_test.id,
            "item_selected": 1,
            "customization": "",
          },
          follow=True
      )
      
      html = response.content.decode("utf8")

      assert "Current Order" in html 
      assert response.status_code == 200
