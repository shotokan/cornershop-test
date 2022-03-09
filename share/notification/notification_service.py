from django.conf import settings

from .slack_notification_client import SlackWrapper


DOMAIN = getattr(settings, "PROJECT_DOMAIN", "http://localhost:8000")


class NotificationService:
    """
    This class is a service to be able to send a notification
    """

    def __init__(self, client):
        self.client = client

    def send_message(self, menu_id):
        """
        Sends a notification to slack

        Parameters:
          menu_id (str): identifier to find the menu
        """
        users = self.client.get_users()
        for user in users:
            message = (
                f"Hello, {user.username}!, see today's menu {DOMAIN}/menu/{menu_id}"
            )
            self.client.send_message(user, message)
