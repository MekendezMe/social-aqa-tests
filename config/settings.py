# BASE_URL = 'https://a-little-bit-api.com.ru/api/v1'

from dotenv import load_dotenv
import os

load_dotenv()

ENV = os.getenv("ENV", "local")
BASE_URL = os.getenv("BASE_URL")
TIMEOUT = int(os.getenv("TIMEOUT", "10"))

if not BASE_URL:
    raise ValueError("BASE_URL is not set")