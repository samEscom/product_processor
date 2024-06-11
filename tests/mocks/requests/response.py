from typing import Dict


class ResponseMock:
    def __init__(self, response, status_code) -> None:
        self.response = response
        self.status_code = status_code
        self.cookies = ""

    def json(self) -> Dict:
        return self.response
