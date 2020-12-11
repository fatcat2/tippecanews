from datetime import datetime

def log(message: str):
    print(f"{datetime.now()}: {message}")

if __name__ == "__main__":
    log("Hello")