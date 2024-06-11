import io
import re
from typing import Dict, List

import requests

from src.aws import AWS
from src.constants import ECOMMERCE_API, ECOMMERCE_PASS, ECOMMERCE_USER
from src.logger import logger


class Product:
    def __init__(self, file: str):
        self.data = []
        self.aws = AWS()
        self.messages_send = []
        self.file_name = file
        self.token = ""

    def __set_data(self, file) -> None:
        data_file = file.decode("utf-8")
        with io.StringIO(data_file) as fp:
            for linea in fp:
                if any(linea):
                    line = linea.strip().split("|")
                    self.data.append(line)
                else:
                    break

    def __create_payload(self, line_product: List) -> Dict:
        if len(line_product) < 79:
            logger.error("Product with characters interpreted as line break")
            return {}
        customs = dict(
            list(
                map(
                    lambda x: (x[0], x[1].strip()),
                    re.findall(r"(\w+)=(\w+)", line_product[38]),
                )
            )
        )
        if not customs or line_product[45] == "" or line_product[55] == "":
            return {}
        dict_ = {
            "sku": line_product[0],
            "name": line_product[6],
            "price": line_product[13] or 0.0,
            "category": line_product[4] or "",
            "extension_attributes": {
                "stock_item": {
                    "min_sale_qty": int(float(line_product[45])),
                    "use_config_min_sale_qty": 1 if line_product[46] in "1" else 0,
                    "use_config_qty_increments": True
                    if line_product[54] in "1"
                    else False,
                    "qty_increments": int(float(line_product[55])),
                    "use_config_enable_qty_inc": True
                    if line_product[46] in "1"
                    else False,
                    "enable_qty_increments": True if line_product[54] in "0" else False,
                    "use_config_backorders": False if line_product[43] in "1" else True,
                    "backorders": 1,
                }
            },
            "custom_attributes": [
                {"attribute_code": "unidad_de_medida", "value": customs["M"]},
                {
                    "attribute_code": "alto",
                    "value": line_product[72] if line_product[72] != "" else "1",
                },
                {
                    "attribute_code": "largo",
                    "value": line_product[75] if line_product[75] != "" else "1",
                },
                {
                    "attribute_code": "peso",
                    "value": line_product[76] if line_product[76] != "" else "1",
                },
                {"attribute_code": "bulto", "value": line_product[77]},
                {"attribute_code": "sat_id", "value": line_product[78]},
            ],
        }
        return {"sku": dict_["sku"], "product": dict_}

    def __send_message(self) -> None:

        for item in self.data:
            payload = self.__create_payload(item)
            message = self.aws.send_event_message(data=payload)

            self.messages_send.append(
                {"token": self.token, "product": payload["sku"], "messageId": message}
            )

    def __get_token(self) -> None:
        url = f"{ECOMMERCE_API}V1/admin/token"
        data = {"username": ECOMMERCE_USER, "password": ECOMMERCE_PASS}
        response = requests.session().post(url, json=data)

        if response.status_code != 200:
            raise RuntimeError("Failed create token with Magento")

        self.token = response.json()

    def execute(self) -> None:
        self.__get_token()
        self.__set_data(self.aws.get_file(self.file_name))
        self.__send_message()
