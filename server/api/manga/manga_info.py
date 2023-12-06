import requests

from entities.manga import Manga
from ..configs import base_url, headers
from ..throw_api_error import throw_api_error

from execution.log_configs import logger


def manga_exists(manga_url: str) -> str:
    url = f"{base_url}/mangas/exists"

    response = requests.post(url, json={"url": manga_url}, headers=headers)
    results = response.json()

    if response.status_code != 200:
        throw_api_error(results)

    return results["data"]


def add_manga(manga: Manga) -> str:
    url = f"{base_url}/mangas/add"

    response = requests.post(url, json=manga.to_dict(), headers=headers)
    results = response.json()

    if response.status_code != 200:
        throw_api_error(results)

    return results["data"]
