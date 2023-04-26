import core.manga
from core.sites.readm import (
    manga_detail,
    get_all_start_with,
    get_latest_updates,
    get_populars,
    get_pages,
)
from ..database import Database, Manga
from .website_handler import WebsiteHandler

import traceback


class ReadmHandler(WebsiteHandler):
    """Class that updates database with readm mangas"""

    def __init__(self, database: Database):
        super().__init__(database=database, origin="readm")
        self.origin = "readm"
        self.language = "english"

    def get_details(self, manga_url: str) -> core.manga.Manga:
        return manga_detail(manga_url=manga_url, show_window=False)

    def get_all_urls(self):
        urls = []

        for letter in [chr(i) for i in range(97, 123)]:
            try:
                letter_urls = get_all_start_with(letter=letter, show_window=False)
                urls = urls + letter_urls
            except Exception:
                print(traceback.format_exc())

        return urls

    def get_latest_updated_urls(self):
        urls = []

        try:
            urls = urls + get_latest_updates(limit=400)
        except Exception:
            print(traceback.format_exc())

        return urls

    def get_popular_urls(self):
        return []

    def get_manga(self, manga_url: str) -> Manga:
        details = manga_detail(manga_url, False)

        chapters = {}
        for chapter_name in details.chapters:
            chapter = self.get_chapter(manga_url, chapter_name)
            chapters.update(chapter)

        manga = Manga(
            title=details.title,
            alternative_title=details.alternative_title,
            author=details.author,
            artist=details.artist,
            status=details.status,
            url=manga_url,
            origin=self.origin,
            language=self.language,
            thumbnail=details.thumbnail,
            genres=details.genres,
            summary=details.summary,
            chapters=chapters,
        )

        return manga

    def get_chapter(self, manga_url: str, chapter_name: str) -> dict[str, list[str]]:
        cp_url = f"{manga_url}/{chapter_name}/all-pages"
        pages = get_pages(cp_url)
        return {chapter_name: pages}
