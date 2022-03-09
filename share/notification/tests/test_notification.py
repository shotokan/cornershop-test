import uuid
import pytest

from unittest import mock

from ..notification_entity import UserNotification
from ..notification_service import NotificationService, DOMAIN


@pytest.fixture
def user_notification_1_test() -> UserNotification:
    user_notification = UserNotification(
        str(uuid.uuid4()), "isabido", "Ivan Sabido", "isabido86@outlook.com"
    )
    return user_notification


@pytest.fixture
def user_notification_2_test() -> UserNotification:
    user_notification = UserNotification(
        str(uuid.uuid4()), "israel", "Israel Sabido", "israel@outlook.com"
    )
    return user_notification


def test_should_send_message_to_user(user_notification_1_test):
    with mock.patch(
        "share.notification.notification_service.SlackWrapper"
    ) as MockSlackWrapper:
        MockSlackWrapper.return_value.get_users.return_value = [
            user_notification_1_test
        ]
        MockSlackWrapper.return_value.send_message.return_value = True
        menu_id = str(uuid.uuid4())
        message = f"Hello, {user_notification_1_test.username}!, see today's menu {DOMAIN}/menu/{menu_id}"
        notification_service = NotificationService(MockSlackWrapper())

        notification_service.send_message(menu_id)

        MockSlackWrapper.return_value.get_users.assert_called_once()
        MockSlackWrapper.return_value.send_message.assert_called_once_with(
            user_notification_1_test, message
        )


def test_should_send_message_to_two_users(
    user_notification_1_test, user_notification_2_test
):
    with mock.patch(
        "share.notification.notification_service.SlackWrapper"
    ) as MockSlackWrapper:
        MockSlackWrapper.return_value.get_users.return_value = [
            user_notification_1_test,
            user_notification_2_test,
        ]
        MockSlackWrapper.return_value.send_message.return_value = True
        menu_id = str(uuid.uuid4())
        message_1 = f"Hello, {user_notification_1_test.username}!, see today's menu {DOMAIN}/menu/{menu_id}"
        message_2 = f"Hello, {user_notification_2_test.username}!, see today's menu {DOMAIN}/menu/{menu_id}"
        notification_service = NotificationService(MockSlackWrapper())

        notification_service.send_message(menu_id)

        MockSlackWrapper.return_value.get_users.assert_called_once()
        MockSlackWrapper.return_value.send_message.assert_any_call(
            user_notification_1_test, message_1
        )
        MockSlackWrapper.return_value.send_message.assert_any_call(
            user_notification_2_test, message_2
        )


def test_should_not_send_message_to_user_when_no_users_in_slack(
    user_notification_1_test,
):
    with mock.patch(
        "share.notification.notification_service.SlackWrapper"
    ) as MockSlackWrapper:
        MockSlackWrapper.return_value.get_users.return_value = []
        MockSlackWrapper.return_value.send_message.return_value = True
        menu_id = str(uuid.uuid4())
        notification_service = NotificationService(MockSlackWrapper())

        notification_service.send_message(menu_id)

        MockSlackWrapper.return_value.get_users.assert_called_once()
        MockSlackWrapper.return_value.send_message.assert_not_called()
