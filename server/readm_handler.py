from core.manga import Manga as MangaDetails
from .entities import Manga
from core.sites.readm import (
    manga_detail as get_manga_details,
    get_pages,
    get_all_start_with,
    get_latest_updates,
)
from .database import MangaDatabase
from time import time
from threading import Thread, Lock, Semaphore


class ReadmHandler:
    def __init__(self, database: MangaDatabase) -> None:
        self.database = database
        self.db_access = Lock()  # mutex for database write control
        self.exec_permissions = Semaphore(3)  # only 3 concurrent threads

    def start(self):
        print("Readm handler started")
        last_update_time = time()

        if self.database.is_empty():
            self._save_all_mangas()

        while True:
            # update mangas every 24 hours
            if time() - last_update_time >= 24 * 60 * 60:
                self._update_latest_mangas()
                last_update_time = time()

    def _update_latest_mangas(self):
        """Updates the latest mangas from readm.org"""
        print("Updating mangas.")
        get_latest_updates(400, self._init_perform_thread)

    def _save_all_mangas(self):
        """Save all mangas from readm in database"""
        print("Downloading mangas for the first time.")
        letters = [chr(i) for i in range(97, 123)]

        for letter in letters:
            get_all_start_with(letter, False, self._init_perform_thread)

    def _init_perform_thread(self, manga_url: str):
        """Start the threads"""
        self.exec_permissions.acquire()  # request permission to run a new thread
        Thread(target=self._perform, args=(manga_url,)).start()

    def _perform(self, manga_url: str):
        """Checks if exists. If true, update it. Otherwise, save for the first time"""
        try:
            initial_time = time()

            if not self.database.exists_by_url(manga_url):
                self._save_manga(manga_url)
                print(f"Stored manga with url '{manga_url}'.")
            else:
                self._update_manga(manga_url)
                print(
                    f"Updated manga with url '{manga_url}'. (duration: {time() - initial_time})"
                )
        except Exception as error:
            print(error)
        finally:
            self.exec_permissions.release()

    def _update_manga(self, manga_url: str):
        """Updates manga to latest version"""
        try:
            current_manga = self.database.get_by_url(manga_url)
            details = get_manga_details(manga_url, False)

            for chapter_name in details.chapters:
                if not chapter_name in current_manga.chapters_names:
                    new_chapter = self._get_chapter(manga_url, chapter_name)
                    current_manga.chapters.update(new_chapter)
                    current_manga.total_chapters += 1
                    current_manga.chapters_names.append(chapter_name)

            self.db_access.acquire()
            self.database.set_by_url(manga_url, current_manga)
            self.db_access.release()
        except Exception as error:
            print(error)

    def _save_manga(self, manga_url):
        """Save manga in database"""
        try:
            manga = self._get_manga(manga_url)

            self.db_access.acquire()
            self.database.add(manga)
            self.db_access.release()
        except Exception as error:
            print(error)

    def _get_manga(self, manga_url: str) -> Manga:
        """Downloads manga and all pages from readm.org"""
        details: MangaDetails = get_manga_details(manga_url, False)

        chapters = {}
        for chapter_name in details.chapters:
            chapter = self._get_chapter(manga_url, chapter_name)
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
            total_chapters=details.total_chapters,
            thumbnail=details.thumbnail,
            genres=details.genres,
            summary=details.summary,
            chapters_names=details.chapters,
            chapters=chapters,
        )

        return manga

    def _get_chapter(self, manga_url: str, chapter_name: str) -> dict:
        """Download manga chapter"""
        cp_url = f"{manga_url}/{chapter_name}/all-pages"
        pages = get_pages(cp_url)
        return {chapter_name: pages}
