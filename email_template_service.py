

from model import NotificationType, User, Email


class EmailTemplateService:
    def generate_email(self, notification_type: NotificationType, user: User) -> Email:
        match notification_type:
            case NotificationType.WELCOME:
                body = f"""
                     Hi {user.name},
                     Welcome to the application.
                     """
                subject = "Welcome to our application."
                return Email(to= user.email,subject= subject,body= body)
        raise ValueError("Invalid notification type")

