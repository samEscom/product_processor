from datetime import datetime
from io import BytesIO

from botocore.response import StreamingBody

file_upload = open("B2B_ART")
file_s3 = bytes(file_upload.read(), "utf-8")
raw_stream = StreamingBody(BytesIO(file_s3), len(file_s3))
file_upload.close()

mock_data = {
    "get_object": {
        "raise_exception": False,
        "response": {
            "ResponseMetadata": {
                "RequestId": "6BFC00970E62BC8F",
                "HTTPStatusCode": 200,
                "RetryAttempts": 1,
            },
            "LastModified": str(datetime(2024, 1, 29, 5, 39, 29)),
            "ContentLength": 58,
            "ETag": '"6299528715bad0e3510d1e4c4952ee7e"',
            "ContentType": "binary/octet-stream",
            "Metadata": {},
            "Body": raw_stream,
        },
    },
    "send_message": {
        "raise_exception": False,
        "response": {
            "MD5OfMessageBody": "137124aa4a8b0bb064b60b6ed80e0c90",
            "MessageId": "585a08f1-a5ee-42d7-a7d2-9b227e5b95bc",
        },
    },
}
