from src.app import main

if __name__ == "__main__":

    event = {"update": False, "file": "products.csv"}

    resp = main(event, None)
    print(resp)
