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

    def get_chapter(self, manga_url: str, info: ChapterInfo) -> Chapter:
        cp_url = f"{manga_url}/{info.name}/all-pages"
        pages = get_pages(cp_url)
        return Chapter(name=info.name, pages=pages)
