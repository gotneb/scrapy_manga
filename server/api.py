import requests
import os
from dotenv import load_dotenv

from entities.manga import Manga
from entities.chapter import Chapter
from entities.website_update import WebsiteUpdate
from errors.api_error import ApiError

load_dotenv()


base_url = os.getenv("API_BASE_URL")
authorization = os.getenv("AUTH_TOKEN")

headers = {"authorization": authorization}


def prepare_url(endpoint: str) -> str:
    return f"{base_url}{endpoint}"


def get_origin_info(origin: str) -> WebsiteUpdate:
    url = prepare_url(f"/info/get/{origin}")

    response = requests.get(url, headers=headers)

    if response.status_code == 404:
        return None

    results = response.json()

    if response.status_code != 200:
        throw_api_error(results)

    return WebsiteUpdate(
        origin=results["data"]["origin"],
        language=results["data"]["language"],
        populars=results["data"]["populars"],
        latest_updates=results["data"]["latest_updates"],
    )


def origin_exists(origin: str) -> bool:
    url = prepare_url(f"/info/get/{origin}")

    response = requests.get(url, headers=headers)
    results = response.json()

    if response.status_code == 404:
        return False

    if response.status_code != 200:
        throw_api_error(results)

    return results["data"] != None


def update_info(info: WebsiteUpdate) -> bool:
    url = prepare_url(f"/info/update")

    response = requests.post(url, json=info.to_dict(), headers=headers)
    results = response.json()

    if response.status_code != 200:
        throw_api_error(results)

    return results["data"]


def add_info(info: WebsiteUpdate) -> bool:
    url = prepare_url(f"/info/add")

    response = requests.post(url, json=info.to_dict(), headers=headers)
    results = response.json()

    if response.status_code != 200:
        throw_api_error(results)

    return results["data"] != None


def manga_exists(manga_url: str) -> str:
    url = prepare_url(f"/mangas/exists")

    response = requests.post(url, json={"url": manga_url}, headers=headers)
    results = response.json()

    if response.status_code != 200:
        throw_api_error(results)

    return results["data"]


def get_chapter_names(manga_id: str) -> list[str]:
    url = prepare_url(f"/chapters/names/{manga_id}")

    response = requests.get(url, headers=headers)
    results = response.json()

    if response.status_code != 200:
        throw_api_error(results)

    return results["data"]


def add_chapters(manga_id: str, chapters: list[Chapter]) -> bool:
    prepared_chapters = list(map(lambda chapter: chapter.to_dict(), chapters))

    body = {"id": manga_id, "chapters": prepared_chapters}

    url = prepare_url(f"/chapters/add")
    response = requests.post(url, json=body, headers=headers)

    results = response.json()

    if response.status_code != 200:
        throw_api_error(results)

    return results["data"]


def add_manga(manga: Manga) -> str:
    url = prepare_url(f"/mangas/add")

    response = requests.post(url, json=manga.to_dict(), headers=headers)
    results = response.json()

    if response.status_code != 200:
        throw_api_error(results)

    return results["data"]


def throw_api_error(results: any):
    if results:
        message = results["error"]
    else:
        message = "unexpected error"

    raise ApiError(message)
