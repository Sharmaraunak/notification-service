

### basic fastapi application for notification service

from fastapi import FastAPI, HTTPException, Depends
from starlette import status
from starlette.requests import Request

from brokers.inmemory_message_broker import InMemoryMessageBroker
from dependencies.dependencies import get_broker
from init_application import lifespan
from models.model import NotificationRequest
from services.email_template_service import EmailTemplateService
from data.user_list import  users



app = FastAPI(lifespan=lifespan)



@app.post("/notification", status_code=status.HTTP_202_ACCEPTED)
async def send_notification(notification: NotificationRequest, message_broker: InMemoryMessageBroker=(Depends(get_broker)), template_service: EmailTemplateService = Depends(EmailTemplateService)):
    user_id = notification.user_id



    try:
        ## find user
        user = users.get(user_id)
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")

        ## generate email from notification type

        email = template_service.generate_email(notification_type=notification.notification_type, user = user)

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

