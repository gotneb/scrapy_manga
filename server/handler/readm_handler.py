from core.sites.readm import (
    manga_detail,
    get_all_start_with,
    get_latest_updates,
    get_populars,
    get_pages,
)
from ..database import Database
from entities import Manga, ChapterInfo, Chapter
from .website_handler import WebsiteHandler

import traceback


class ReadmHandler(WebsiteHandler):
    """Class that updates database with readm mangas"""

    def __init__(self, database: Database):
        super().__init__(database=database, origin="readm")
        self.origin = "readm"
        self.language = "english"

    def get_all_urls(self):
        urls = []

        for letter in [chr(i) for i in range(97, 123)]:
            try:
                letter_urls = get_all_start_with(letter=letter)
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
        manga = manga_detail(manga_url, False)
        manga.chapters = []

        for info in manga.chapters_info:
            chapter = self.get_chapter(manga_url, info)
            manga.chapters.append(chapter)

        return manga

    def get_chapter(self, manga_url: str, info: ChapterInfo) -> Chapter:
        cp_url = f"{manga_url}/{info.name}/all-pages"
        pages = get_pages(cp_url)
        return Chapter(name=info.name, pages=pages)
