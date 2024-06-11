from json import dumps
from typing import Dict

from src.logger import logger
from src.product import Product


def main(event, context) -> Dict:

    logger.info("PRODUCT EVENT: %s", event["file"])

    product = Product(event["file"])
    product.execute()

    response = {
        "statusCode": 200,
        "body": dumps(
            {
                "messagesSend": product.messages_send,
                "total": len(product.messages_send)
            }
        )
    }
    logger.info(response)
    return response
