import boto3
import json
import requests
import pytest
from index import handler
from tests.mocks.inputs import mock_data

from .mocks.boto3_client import Boto3ClientMock

from datetime import datetime
from io import BytesIO

from botocore.response import StreamingBody
from .mocks.requests.requests import RequestMock
from src.constants import ECOMMERCE_API


file_upload = open("B2B_ART")
file_s3 = bytes(file_upload.read(), "utf-8")
raw_stream = StreamingBody(BytesIO(file_s3), len(file_s3))
file_upload.close()


def test_send_message(monkeypatch):
    def mock_boto3client_success(_, **kwargs):
        return Boto3ClientMock(_, mock_data=mock_data)

    def mock_requests_session():
        return RequestMock(
            mock_data={
                f"{ECOMMERCE_API}V1/admin/token": {
                    "raise_exception": False,
                    "response": "12345678",
                    "status_code": 200,
                },
            }
        )

    monkeypatch.setattr(boto3, "client", mock_boto3client_success)
    monkeypatch.setattr(requests, "session", mock_requests_session)

    response = handler(
        event={
            "update": True,
            "file": "B2B_ART"
        },
        context=None,
    )

    assert response["statusCode"] == 200

    resp = json.loads(response["body"])
    assert isinstance(resp["messagesSend"], list)
    assert resp["total"] == 5


def test_fail_send_message(monkeypatch):

    def mock_boto3client_success(_, **kwargs):
        return Boto3ClientMock(_, mock_data={
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
                "raise_exception": True,
                "response": None
            },
        })

    def mock_requests_session():
        return RequestMock(
            mock_data={
                f"{ECOMMERCE_API}V1/admin/token": {
                    "raise_exception": False,
                    "response": "12345678",
                    "status_code": 200,
                },
            }
        )

    monkeypatch.setattr(boto3, "client", mock_boto3client_success)
    monkeypatch.setattr(requests, "session", mock_requests_session)

    response = handler(
        event={
            "update": True,
            "file": "B2B_ART"
        },
        context=None,
    )

    assert response["statusCode"] == 200
    body = json.loads(response["body"])
    assert isinstance(body["messagesSend"], list)
    assert body["total"] == 5

    messages_send = body["messagesSend"]

    for i in messages_send:
        assert i["messageId"] is None


def test_fail_login(monkeypatch):

    def mock_requests_session():
        return RequestMock(
            mock_data={
                f"{ECOMMERCE_API}V1/admin/token": {
                    "raise_exception": False,
                    "response": False,
                    "status_code": 500,
                },
            }
        )

    monkeypatch.setattr(requests, "session", mock_requests_session)

    with pytest.raises(RuntimeError):
        handler(
            event={
                "update": True,
                "file": "B2B_ART"
            },
            context=None,
        )
