
### basic fastapi application for notification service
import threading

from fastapi import FastAPI, HTTPException
from starlette import status

from brokers.inmemory_message_broker import InMemoryMessageBroker
from models.model import NotificationRequest
from providers.email_provider import EmailProvider

from services.email_template_service import EmailTemplateService
from data.user_list import  users
from workers.email_worker import EmailWorker

app = FastAPI()

message_broker: InMemoryMessageBroker = InMemoryMessageBroker()
email_provider: EmailProvider = EmailProvider()
worker: EmailWorker = EmailWorker(email_provider, message_broker)

thread = threading.Thread(target=worker.run)
thread.start()


@app.post("/notification", status_code=status.HTTP_202_ACCEPTED)
async def send_notification(notification: NotificationRequest, ):
    user_id = notification.user_id
    email_template_service: EmailTemplateService = EmailTemplateService()


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
            ## implementing an in-memory queue
            message_broker.publish(email)
            return {"message": "Email send request accepted"}

    except HTTPException as e:
        raise e

    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")

