from .response import ResponseMock


class RequestMock:
    headers = {}

    def __init__(self, **kwargs) -> None:
        self.mock_data = kwargs["mock_data"]

    def post(self, url, **kwargs):
        url_data = self.mock_data.get(url, {})
        if url_data.get("raise_exception", False):
            raise "Mock Requests Exception"
        return ResponseMock(
            url_data.get("response", {}), url_data.get("status_code", 200)
        )
