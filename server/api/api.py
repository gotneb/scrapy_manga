import requests
import os
from dotenv import load_dotenv

from entities.manga import Manga
from entities.chapter import Chapter
from entities.website_update import WebsiteUpdate
from errors.api_error import ApiError

load_dotenv()


class API:
    def __init__(self, auth_token: str, base_url: str) -> None:
        self.session = requests.Session()
        self.session.headers = {"authorization": auth_token}
        self.base_url = base_url

    def prepare_url(self, endpoint: str) -> str:
        return f"{self.base_url}{endpoint}"

    def origin_exists(self, origin: str) -> bool:
        url = self.prepare_url(f"/info/get/{origin}")
        response = self.session.get(url)
        results = response.json()

        if response.status_code == 404:
            return False

        if response.status_code != 200:
            raise ApiError(results["error"])

        return results["data"] != None

    def update_info(self, info: WebsiteUpdate) -> bool:
        url = self.prepare_url(f"/info/update")
        response = self.session.post(url, json=info.to_dict())
        results = response.json()

        if response.status_code != 200:
            raise ApiError(results["error"])

        return results["data"]

    def add_info(self, info: WebsiteUpdate) -> bool:
        url = self.prepare_url(f"/info/add")
        response = self.session.post(url, json=info.to_dict())
        results = response.json()

        if response.status_code != 200:
            raise ApiError(results["error"])

        return results["data"] != None

    def manga_exists(self, manga_url: str) -> str:
        url = self.prepare_url(f"/mangas/exists")
        response = self.session.post(url, json={"url": manga_url})
        results = response.json()

        if response.status_code != 200:
            raise ApiError(results["error"])

        return results["data"]

    def get_chapter_names(self, manga_id: str) -> list[str]:
        url = self.prepare_url(f"/chapters/names/{manga_id}")
        response = self.session.get(url)
        results = response.json()

        if response.status_code != 200:
            raise ApiError(results["error"])

        return results["data"]

    def add_chapters(self, manga_id: str, chapters: list[Chapter]) -> bool:
        prepared_chapters = list(map(lambda chapter: chapter.to_dict(), chapters))

        print(prepared_chapters)
        body = {"id": manga_id, "chapters": prepared_chapters}

        url = self.prepare_url(f"/chapters/add")
        response = self.session.post(url, json=body)

        results = response.json()

        if response.status_code != 200:
            raise ApiError(results["error"])

        return results["data"]

    def add_manga(self, manga: Manga) -> str:
        url = self.prepare_url(f"/mangas/add")
        response = self.session.post(url, json=manga.to_dict())
        results = response.json()

        if response.status_code != 200:
            raise ApiError(results["error"])

        return results["data"]


api = API(auth_token=os.getenv("AUTH_TOKEN"), base_url=os.getenv("API_BASE_URL"))
