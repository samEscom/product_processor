from src.app import main


def handler(event, context):
    return main(event, context)
