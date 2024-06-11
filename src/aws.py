import boto3

from json import dumps
from typing import Any, Dict, Optional

from botocore.client import Config

from src.constants import (
    AWS_REGION_EAST,
    AWS_SERVICE_SQS,
    AWS_SERVICE_S3,
    BUCKET_NAME,
    QUEUE_URL,
)
from src.logger import logger


class AWS:

    @staticmethod
    def get_client(service: str):
        return boto3.client(
            service,
            region_name=AWS_REGION_EAST,
            config=Config(signature_version="s3v4"),
        )

    def send_event_message(self, data: Dict) -> Optional[str]:
        sqs_client = self.get_client(AWS_SERVICE_SQS)

        try:
            response = sqs_client.send_message(
                QueueUrl=QUEUE_URL,
                DelaySeconds=1,
                MessageBody=dumps(data),
            )
            logger.info("Sending message: %s", str(response))
            return response['MessageId']
        except Exception as e:
            logger.error("Error sending message: %s", str(e))
            return None

    def get_file(self, file_name: str) -> Any:
        try:
            s3 = self.get_client(AWS_SERVICE_S3)
            response = s3.get_object(Bucket=BUCKET_NAME, Key=file_name)

            return response["Body"].read()

        except Exception:
            raise
