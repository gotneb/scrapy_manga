from core.manga import Manga as MangaDetails
from core.sites.readm import *
from ..database import *
from time import time, sleep
from concurrent.futures import ThreadPoolExecutor, wait
from threading import Thread


class ReadmHandler(Thread):
    """Class that updates database with readm mangas"""

    def __init__(self, database: MangaDatabase) -> None:
        Thread.__init__(self)
        self.database = database
        self.executor = ThreadPoolExecutor(max_workers=4)
        self.futures = []

    def run(self):
        """Executes when calling method start ( of the superclass Thread)"""
        print("::----- Readm Handler Started -----::")

        while True:
            last_update_time = time()

            if self.database.is_empty(origin="readm"):
                self.populate_database()
            else:
                self.update_database()

            wait(self.futures)
            self.futures.clear()

            update_duration = time() - last_update_time

            print("::----- Readm Handler Completed -----::")
            sleep(24 * 60 * 60 - update_duration)

    def populate_database(self):
        """Iterates over all links and stores manga in database"""
        for letter in [chr(i) for i in range(97, 123)]:
            get_all_start_with(
                letter=letter,
                show_window=False,
                on_link_received=self.create_perform_thread,
            )

    def update_database(self):
        """Iterates over all latest updates links and updates manga in the database"""
        get_latest_updates(
            limit=40,
            on_link_received=self.create_perform_thread,
        )

    def create_perform_thread(self, manga_url: str):
        """Creates thread that executes method perform()"""
        future = self.executor.submit(self.perform, manga_url)
        self.futures.append(future)

    def perform(self, manga_url: str):
        """Checks if exists. If true, update it. Otherwise, save for the first time"""
        print(f"Processing: {manga_url}.")
        if not self.database.exists(manga_url):
            self.save_manga(manga_url)
        else:
            self.update_manga(manga_url)

    def update_manga(self, manga_url: str):
        """Updates manga to latest version"""
        try:
            current_manga = self.database.get(manga_url)
            details = manga_detail(manga_url, False)
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

    def get_manga(self, manga_url: str) -> Manga:
        """Downloads manga and all pages from readm.org"""
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
        """Download manga chapter"""
        cp_url = f"{manga_url}/{chapter_name}/all-pages"
        pages = get_pages(cp_url)
        return {chapter_name: pages}
