import os
from dotenv import load_dotenv

load_dotenv()


base_url = os.getenv("API_BASE_URL")
_authorization = os.getenv("AUTH_TOKEN")

headers = {"authorization": _authorization}
