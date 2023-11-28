import requests

from entities.manga import Chapter
from ..configs import base_url, headers
from ..throw_api_error import _throw_api_error


def get_chapter_names(manga_id: str) -> list[str]:
    url = f"{base_url}/chapters/names/{manga_id}"

    response = requests.get(url, headers=headers)
    results = response.json()

    if response.status_code != 200:
        _throw_api_error(results)

    return results["data"]


def add_chapters(manga_id: str, chapters: list[Chapter]) -> bool:
    prepared_chapters = list(map(lambda chapter: chapter.to_dict(), chapters))

    body = {"id": manga_id, "chapters": prepared_chapters}

    url = f"{base_url}/chapters/add"
    response = requests.post(url, json=body, headers=headers)

    results = response.json()

    if response.status_code != 200:
        _throw_api_error(results)

    return results["data"]
