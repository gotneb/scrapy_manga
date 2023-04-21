from abc import ABC, abstractmethod
from ..database import Manga, Database
from threading import Thread
from core.manga import Manga as MangaDetail
from time import time, sleep


class WebsiteHandler(ABC, Thread):
    """Base class for websites handlers"""

    def __init__(
        self,
        database: Database,
        get_manga_detail,
        get_all_start_with,
        get_latest_updates,
    ) -> None:
        Thread.__init__(self)
        self.database = database
        self.get_manga_detail = get_manga_detail
        self.get_all_start_with = get_all_start_with
        self.get_latest_updates = get_latest_updates

    def run(self):
        """Executes when calling method start ( of the superclass Thread)"""
        print("Readm handler: started.")

        if self.database.is_empty(origin="readm"):
            self.populate_database()
        else:
            self.update_database()

        print("Readm handler: done.")

    def populate_database(self):
        """Iterates over all links and stores manga in database"""
        for letter in [chr(i) for i in range(97, 123)]:
            self.get_all_start_with(
                letter=letter,
                show_window=False,
                on_link_received=self.perform,
            )

    def update_database(self):
        """Iterates over all latest updates links and updates manga in the database"""
        self.get_latest_updates(
            limit=40,
            on_link_received=self.perform,
        )

    def perform(self, manga_url: str):
        """Checks if exists. If true, update it. Otherwise, save for the first time"""
        print(f"Readm handler: processing {manga_url}.")
        if not self.database.exists(manga_url):
            self.save_manga(manga_url)
        else:
            self.update_manga(manga_url)

    def update_manga(self, manga_url: str):
        """Updates manga to latest version"""
        try:
            current_manga = self.database.get(manga_url)
            details = self.get_manga_detail(manga_url, False)
            chapter_names = list(current_manga.chapters.keys())

            for chapter_name in details.chapters:
                if not chapter_name in chapter_names:
                    new_chapter = self.get_chapter(manga_url, chapter_name)
                    current_manga.chapters.update(new_chapter)

            self.database.set(manga_url, current_manga)
        except Exception as error:
            print(error)

    def save_manga(self, manga_url):
        """Save manga in database"""
        try:
            manga = self.get_manga(manga_url)
            self.database.add(manga)
        except Exception as error:
            print(error)

    @abstractmethod
    def get_manga(self, manga_url: str) -> Manga:
        """Downloads manga and all pages from readm.org"""
        pass

    @abstractmethod
    def get_chapter(self, manga_url: str, chapter_name: str) -> dict:
        """Downloads manga chapter pages"""
        pass
