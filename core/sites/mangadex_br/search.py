from requests import get
from .constants import base_url

def search(title: str) -> None:
    r = get(
    f"{base_url}/manga",
    params={"title": title}
    )
    print([manga["id"] for manga in r.json()["data"]])
    