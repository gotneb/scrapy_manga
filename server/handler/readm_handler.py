from core.manga import Manga as MangaDetails
from core.sites.readm import *
from ..database import Database
from .website_handler import WebsiteHandler


class ReadmHandler(WebsiteHandler):
    """Class that updates database with readm mangas"""

    def __init__(self, database: Database):
        super().__init__(
            database=database,
            get_manga_detail=manga_detail,
            get_all_start_with=get_all_start_with,
            get_latest_updates=get_latest_updates,
        )
        self.database = database

    def get_manga(self, manga_url: str) -> Manga:
        details: MangaDetails = manga_detail(manga_url, False)

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
            origin="readm",
            language="english",
            thumbnail=details.thumbnail,
            genres=details.genres,
            summary=details.summary,
            chapters=chapters,
        )

        return manga

    def get_chapter(self, manga_url: str, chapter_name: str) -> dict:
        cp_url = f"{manga_url}/{chapter_name}/all-pages"
        pages = get_pages(cp_url)
        return {chapter_name: pages}
