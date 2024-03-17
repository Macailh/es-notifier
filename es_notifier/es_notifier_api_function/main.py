import boto3
from fastapi import FastAPI, HTTPException
from botocore.exceptions import ClientError

app = FastAPI()
sns_client = boto3.client("sns")
ses_client = boto3.client("ses")


@app.get("/")
def root():
    return {"message": "root"}


@app.post("/emails")
def send_email():
    try:
        response = ses_client.send_email(
            Source="example_source@mail.com",
            Destination={
                "ToAddresses": [
                    "example_destination@mail.com",
                ]
            },
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
def send_sms():
    try:
        response = sns_client.publish(
            PhoneNumber="+521234567890", Message="Example message"
        )

        return response
    except ClientError as e:
        raise HTTPException(status_code=400, detail=str(e))
