from abc import ABC, abstractmethod
from ..database import Manga, Database, WebsiteUpdate
from threading import Thread
import core.manga
import traceback
from concurrent.futures import ThreadPoolExecutor, Future, wait


class WebsiteHandler(ABC, Thread):
    """Base class for websites handlers."""

    def __init__(self, database: Database, origin: str) -> None:
        Thread.__init__(self)
        self.db = database
        self.origin = origin
        self.number_of_works = 3  # Set this value according to your preference (affects the computer's performance)

    def run(self):
        """Get the manga urls and update the database."""

        print(f"Handler ({self.origin}): started.")

        print(f"Handler ({self.origin}): downloading latest updated urls.")
        latest_updated_urls = self.get_latest_updated_urls()

        print(f"Handler ({self.origin}): downloading the most popular urls.")
        popular_urls = self.get_popular_urls()

        update_info = WebsiteUpdate(
            origin=self.origin,
            populars=popular_urls,
            latest_updates=latest_updated_urls,
        )

        self.db.set_update_info(update_info)  # update website info in database

        if self.db.is_empty(self.origin):
            print(f"Handler ({self.origin}): downloading all urls.")
            urls = self.get_all_urls()
        else:
            urls = latest_updated_urls

        with ThreadPoolExecutor(max_workers=self.number_of_works) as executor:
            futures: list[Future] = []

            for url in urls:
                futures.append(executor.submit(self.feat, url))

            executor.shutdown(wait=True)

        print(f"Handler ({self.origin}): finished.")

    def feat(self, manga_url: str):
        """Check if manga is in the database, saving the manga or updating chapters."""
        try:
            print(f"Handler ({self.origin}): processing {manga_url}")
            manga_exists = self.db.exists(manga_url)

            if manga_exists:
                self.update(manga_url)
            else:
                self.save(manga_url)
        except Exception:
            print(
                f"Handler ({self.origin}) failure: {manga_url}\n      {traceback.format_exc()}"
            )

    def update(self, manga_url: str):
        """Checks for missing chapters and updates them."""
        manga_details = self.get_details(manga_url)
        manga = self.db.get(manga_url)

        chapter_names = [
            item
            for item in manga_details.chapters
            if item not in manga.get_chapter_names()
        ]

        for name in chapter_names:
            chapter = self.get_chapter(manga_url, name)
            manga.chapters.update(chapter)

        self.db.set(manga.url, manga)

    def save(self, manga_url: str):
        """Save a new manga in the database."""
        manga = self.get_manga(manga_url)
        self.db.add(manga)

    @abstractmethod
    def get_details(self, manga_url: str) -> core.manga.Manga:
        """Get the manga details (core.manga.Manga)."""
        pass

    @abstractmethod
    def get_manga(self, manga_url: str) -> Manga:
        """Get the manga entity (server.entities.Manga)."""
        pass

    @abstractmethod
    def get_chapter(self, manga_url: str, chapter_name: str) -> dict[str, list[str]]:
        """get a chapter in dictionary format: {<chapter_name>: <url_array>}."""
        pass

    @abstractmethod
    def get_all_urls(self) -> list[str]:
        """Return a list of all URLs."""
        pass

    @abstractmethod
    def get_latest_updated_urls(self) -> list[str]:
        """Return a list of latest updated urls."""
        pass

    @abstractmethod
    def get_popular_urls(self) -> list[str]:
        """Return a list of popular manga urls."""
        pass
