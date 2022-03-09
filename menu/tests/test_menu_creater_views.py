import uuid
from unittest import mock

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
def menu_option_1_test(db, today_menu_test) -> MenuItem:
    option = MenuItem()
    option.menu = today_menu_test
    option.description = "Corn pie, Salad and Dessert"
    option.save()
    return option


@pytest.fixture
def menu_option_2_test(db, today_menu_test) -> MenuItem:
    option = MenuItem()
    option.menu = today_menu_test
    option.description = "Chicken Nugget Rice, Salad and Dessert"
    option.save()
    return option


@pytest.fixture
def menu_option_3_test(db, today_menu_test) -> MenuItem:
    option = MenuItem()
    option.menu = today_menu_test
    option.description = "Rice with hamburger, Salad and Dessert"
    option.save()
    return option


def test_should_get_the_form_to_create_a_menu(client, admin_user):
    client.force_login(admin_user)
    response = client.get("/menu/create/")
    assert response.status_code == 200


def test_should_not_get_the_form_to_create_a_menu_no_admin_ser(client, user_test):
    client.force_login(user_test)
    client.login(username=user_test.username, password=user_test.password)
    response = client.get("/menu/create/")
    assert response.status_code == 403


def test_should_get_a_redirect_to_the_form_to_select_a_menu(
    client,
    user_test,
    today_menu_test,
):
    client.force_login(user_test)
    client.login(username=user_test.username, password=user_test.password)
    response = client.get(f"/menu/{today_menu_test.uuid}")

    assert response.status_code == 302


def test_should_get_the_form_to_select_a_menu_without_session(
    client,
    today_menu_test,
):
    response = client.get(f"/menu/{today_menu_test.uuid}", follow=True)

    assert response.status_code == 200


def test_should_get_a_redirect_to_the_form_to_select_a_menu_without_session(
    client,
    today_menu_test,
):
    response = client.get(f"/menu/{today_menu_test.uuid}", follow=True)
    last_url, status_code = response.redirect_chain[-1]

    assert status_code == 302
    assert last_url == f"/staff/menu/{today_menu_test.uuid}"


def test_should_get_bad_request_trying_to_redirect_the_form_to_select_a_menu_without_session(
    client,
    today_menu_test,
):
    response = client.get(f"/menu/1")
    assert response.status_code == 404


@pytest.mark.django_db
def test_should_create_a_menu_admin_user(client, admin_user):
    client.force_login(admin_user)
    client.login(username=admin_user.username, password=admin_user.password)
    response = client.post(
        "/menu/create/",
        {
            "date_month": 3,
            "date_day": 9,
            "date_year": 2022,
            "has_items-TOTAL_FORMS": 4,
            "has_items-INITIAL_FORMS": 0,
            "has_items-MIN_NUM_FORMS": 0,
            "has_items-MAX_NUM_FORMS": 1000,
            "has_items-0-id": "",
            "has_items-0-menu": "",
            "has_items-0-description": "example",
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
    options = MenuItem.objects.all()
    assert len(today_menu) == 1
    assert len(options) == 4
    assert options[0].description == "example"
    assert options[1].description == "example2"
    assert options[2].description == "example3"
    assert options[3].description == "example4"
    assert response.status_code == 302

