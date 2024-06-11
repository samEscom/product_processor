from typing import Dict


class Boto3ClientMock:
    def __init__(self, _, **kwargs) -> None:
        self.mock_data = kwargs["mock_data"]

    def get_object(self, **kwargs) -> Dict:
        data = self.mock_data["get_object"]
        if data.get("raise_exception"):
            raise "Mock AWS Exception"
        return data.get("response", {})

    def send_message(self, **kwargs) -> Dict:
        data = self.mock_data["send_message"]
        if data.get("raise_exception"):
            raise "Mock AWS Exception"
        return data.get("response", {})
