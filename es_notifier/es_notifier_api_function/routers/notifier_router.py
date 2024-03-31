from botocore.exceptions import ClientError
from fastapi import APIRouter, HTTPException
from services.email_service import send_email, send_email_to_topic
from services.sms_service import send_sms

router = APIRouter()


@router.post("/emails")
def send_email_route(recipient: str, subject: str, message: str):
    try:
        send_email(recipient, subject, message)
        return {"message": "Email send successfully"}
    except ClientError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@router.post("/sms")
def send_sms_route(recipient: str, message: str):
    try:
        send_sms(recipient, message)
        return {"message": "SMS send successfully"}
    except ClientError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@router.post("/topics/emails")
def send_email_to_topic_route(recipient: str, message: str):
    try:
        send_email_to_topic(recipient, message)
        return {"message": "Email send successfully"}
    except ClientError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
