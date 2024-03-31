import boto3
import logging
from botocore.exceptions import ClientError
from config.env import SENDER

ses_client = boto3.client("ses")

ses_client_v2 = boto3.client("sesv2")


def send_email(recipient: str, subject: str, message: str):
    try:
        ses_client.send_email(
            Source=SENDER,
            Destination={"ToAddresses": [recipient]},
            Message={
                "Subject": {"Data": subject},
                "Body": {
                    "Text": {"Data": message},
                    "Html": {"Data": f"<p>{message}</p>"},
                },
            },
        )
        return {"message": "Email send successfully"}
    except ClientError as e:
        logging.error(e)
        raise e


def send_email_to_topic(recipient: str, message: str):
    try:
        ses_client_v2.send_email(
            FromEmailAddress=SENDER,
            Destination={"ToAddresses": [recipient]},
            Content={
                "Simple": {
                    "Body": {
                        "Html": {"Charset": "UTF-8", "Data": message},
                        "Text": {"Charset": "UTF-8", "Data": message},
                    },
                    "Subject": {"Charset": "UTF-8", "Data": message},
                    "Headers": [
                        {
                            "Name": "List-Unsubscribe",
                            "Value": "<https://example.com/?address=x&topic=x>",
                        },
                        {
                            "Name": "List-Unsubscribe-Post",
                            "Value": "List-Unsubscribe=One-Click",
                        },
                    ],
                }
            },
        )
        return {"message": "Email send successfully"}
    except ClientError as e:
        logging.error(e)
        raise e
