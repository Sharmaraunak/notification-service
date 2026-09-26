
### basic fastapi application for notification service

from fastapi import FastAPI, HTTPException

from email_provider import EmailProvider
from model import NotificationRequest

from email_template_service import EmailTemplateService
from user_list import  users

app = FastAPI()



@app.post("/notification")
async def send_notification(notification: NotificationRequest):
    user_id = notification.user_id
    email_template_service: EmailTemplateService = EmailTemplateService()
    email_provider: EmailProvider = EmailProvider()

    try:
        ## find user
        user = users.get(user_id)
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")

        ## generate email from notification type

        email = email_template_service.generate_email(notification_type=notification.notification_type, user = user)

        if email is None:
            raise HTTPException(status_code=404, detail="Email not found")
        else:
            email_provider.send_email(email = email)
            return {"message": "Notification sent successfully"}

    except HTTPException as e:
        raise e

    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")

