
from pydantic import BaseModel
from enum import Enum

class NotificationType(Enum):
    WELCOME = "WELCOME"
    PASSWORD_RESET = "PASSWORD_RESET"
    ORDER_SHIPPING = "ORDER_SHIPPING"

class NotificationRequest(BaseModel):
    user_id: int
    notification_type:NotificationType


class User(BaseModel):
    user_id: int
    email: str
    name: str

class Email:
    def __init__(self, to, subject, body):
        self.to = to
        self.subject = subject
        self.body = body
