import logging

logging.basicConfig(
    level=logging.INFO, format="[%(levelname)s] [%(asctime)s] [%(filename)s:%(lineno)d)]: %(message)s"
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
