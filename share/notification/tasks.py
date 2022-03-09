from celery.utils.log import get_task_logger

from backend_test.celery import app

from .notification_service import NotificationService
from .slack_notification_client import SlackWrapper

logger = get_task_logger(__name__)


@app.task(name="send_menu_notification")
def send_menu_notification(menu_id):
    """
    This functions is used as a celery task to sent a notification through celery
    """
    logger.info("sending...")
    client = SlackWrapper()
    notification = NotificationService(client)
    notification.send_message(menu_id)
