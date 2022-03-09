from typing import List

from django.conf import settings

from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

from .notification_entity import UserNotification

SLACK_TOKEN = getattr(settings, "SLACK_TOKEN", None)


class SlackWrapper:
    def __init__(self):
        self.client = WebClient(token=SLACK_TOKEN)

    def send_message(self, user: UserNotification, message: str) -> bool:
        """
        Send a message to a slack user
        returns true when the message was sent
        """
        try:
            self.client.chat_postMessage(channel=user.notification_id, text=message)
            return True
        except SlackApiError as e:
            print(e.response["error"])
            raise e

    def get_users(self) -> List[UserNotification]:
        """
        Get all users that are in a slcak workspace and return a
        list with all them
        """
        try:
            users = []
            slack_users = self.client.users_list()
            for user in slack_users.data["members"]:
                if not self.__is_bot(user):
                    print(user)
                    users.append(
                        UserNotification(
                            user["id"],
                            user["name"],
                            user["real_name"],
                            user["profile"].get("email", ""),
                        )
                    )
            return users
        except SlackApiError as e:
            print(e.response["error"])
            raise e

    def __is_bot(self, user_info: dict) -> bool:
        """
        Verify if a user is a slack bot
        """
        key_to_lookup = "is_bot"
        if key_to_lookup not in user_info or not user_info[key_to_lookup]:
            return False
        return True
