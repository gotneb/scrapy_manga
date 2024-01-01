from requests import get
from .constants import base_url

def get_pages(chapter_id: str) -> list[str]:
    r = get(f'{base_url}/at-home/server/{chapter_id}')

    json = r.json()
    url = json['baseUrl']
    hash = json['chapter']['hash']
    data = json['chapter']['data']

    return [f'{url}/data/{hash}/{p}' for p in data]