import boto3
from botocore.exceptions import ClientError
from config.env import SENDER
from fastapi import APIRouter, HTTPException

router = APIRouter()
ses_client = boto3.client("ses")
sns_client = boto3.client("sns")


@router.post("/emails")
def send_email(recipient: str):
    try:
        ses_client.send_email(
            Source=SENDER,
            Destination={"ToAddresses": [recipient]},
            Message={
                "Subject": {"Data": "Example subject"},
                "Body": {
                    "Text": {"Data": "Example body"},
                    "Html": {"Data": "<h2>Example body</h2>"},
                },
            },
        )
        return {"message": "Email send successfully"}
    except ClientError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@router.post("/sms")
def send_sms(recipient: str, message: str):
    try:
        sns_client.publish(PhoneNumber=recipient, Message=message)

        return {"message": "SMS send successfully"}
    except ClientError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
