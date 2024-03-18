import boto3
from fastapi import FastAPI, HTTPException
from botocore.exceptions import ClientError
from dotenv import load_dotenv
import os
import uvicorn

load_dotenv(dotenv_path=".env.local", override=True)

SENDER = os.getenv("SENDER", "")

app = FastAPI()
sns_client = boto3.client("sns")
ses_client = boto3.client("ses")


@app.post("/emails")
def send_email(recipient: str):
    try:
        response = ses_client.send_email(
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
        return response
    except ClientError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/sms")
def send_sms(recipient: str, message: str):
    try:
        response = sns_client.publish(PhoneNumber=recipient, Message=message)

        return response
    except ClientError as e:
        raise HTTPException(status_code=400, detail=str(e))


if __name__ == "__main__":
    uvicorn.run("local:app", host="localhost", port=8000)
