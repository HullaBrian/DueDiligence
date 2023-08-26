import os

from dotenv import load_dotenv


load_dotenv()


def get_token() -> str:
    return str(os.getenv("TOKEN"))
