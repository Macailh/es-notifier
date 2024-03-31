import boto3
from botocore.exceptions import ClientError

sns_client = boto3.client("sns")


def send_sms(recipient: str, message: str):
    try:
        sns_client.publish(PhoneNumber=recipient, Message=message)

        return {"message": "SMS send successfully"}
    except ClientError as e:
        raise e
