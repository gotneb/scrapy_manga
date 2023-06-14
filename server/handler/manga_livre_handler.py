from core.sites.manga_livre import (
    manga_detail,
    get_all_start_with,
    get_latest_updates,
    get_populars,
    get_pages,
)
from ..database import Database
from entities import Manga, ChapterInfo, Chapter
from .website_handler import WebsiteHandler
import re
import traceback


class MangaLivreHandler(WebsiteHandler):
    """Class that updates database with Manga Livre mangas"""

    def __init__(self):
        self.origin = "manga_livre"
        self.language = "portuguese"

        super().__init__(
            origin=self.origin,
            language=self.language,
            control_file_name=f"{self.origin}_urls.txt",
        )

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
        urls = []

        try:
            urls = urls + get_populars()
        except Exception:
            print(traceback.format_exc())

        return urls

    def get_manga(self, manga_url: str) -> Manga:
        return manga_detail(manga_url, False)

    def get_manga_with_chapter_pages(self, manga_url: str) -> Manga:
        manga = manga_detail(manga_url, False)
        manga.chapters = []

        for info in manga.chapters_info:
            chapter = self.get_chapter(manga_url, info)
            manga.chapters.append(chapter)

        return manga

    def get_chapter(self, manga_url: str, info: ChapterInfo) -> Chapter:
        pattern = r"manga/([^/]+)"
        slug = re.search(pattern=pattern, string=manga_url).group(1)

        cp_url = f" https://mangalivre.net/ler/{slug}/online/{info.id}/{info.name}"
        pages = get_pages(cp_url)

        return Chapter(name=info.name, pages=pages)
