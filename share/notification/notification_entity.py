class UserNotification:
    def __init__(self, notification_id: str, username: str, real_name: str, email: str):
        self.notification_id = notification_id
        self.username = username
        self.real_name = real_name
        self.email = email

    def __str__(self):
        return f"name: {self.real_name} username: {self.username}"
