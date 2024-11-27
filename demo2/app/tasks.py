from celery import Celery
from .config import Config

celery_app = Celery(
    "notification_tasks",
    broker=Config.CELERY_BROKER_URL,
    backend=Config.CELERY_RESULT_BACKEND,
)

@celery_app.task
def send_notification(email: str, message: str):
    # 模拟发送预约通知
    print(f"Sending notification to {email}: {message}")
    return f"Notification sent to {email}."
