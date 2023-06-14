from entities import Manga, ChapterInfo, Chapter, WebsiteUpdate
from threading import Thread
import traceback
from concurrent.futures import ThreadPoolExecutor, Future
from ..api import *
from abc import ABC, abstractmethod


class WebsiteHandler(ABC, Thread):
    """Base class for websites handlers."""

    def __init__(self, origin: str, language: str) -> None:
        Thread.__init__(self)
        self.origin = origin
        self.language = language

        self.number_of_works = 3  # Set this value according to your preference (affects the computer's performance)

    def run(self):
        """Get the manga urls and update the database."""

        print(f"Handler ({self.origin}): started.")

        print(f"Handler ({self.origin}): downloading latest updated urls.")
        latest_updated_urls = self.get_latest_updated_urls()

        print(f"Handler ({self.origin}): downloading the most popular urls.")
        popular_urls = self.get_popular_urls()

        info = WebsiteUpdate(
            origin=self.origin,
            language=self.language,
            populars=popular_urls,
            latest_updates=latest_updated_urls,
        )

        if origin_exists(info.origin):
            update_info(info)
            urls = latest_updated_urls
        else:
            add_info(info)

            print(f"Handler ({self.origin}): downloading all urls.")
            urls = self.get_all_urls()

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
            manga_id = manga_exists(manga_url)

            if manga_id:
                self.update(manga_id, manga_url)
            else:
                self.save(manga_url)
        except Exception:
            print(
                f"Handler ({self.origin}) failure: {manga_url}\n      {traceback.format_exc()}"
            )

    def update(self, manga_id: str, manga_url):
        """Checks for missing chapters and updates them."""
        manga = self.get_manga(manga_url)
        chapter_names_registered = get_chapter_names(manga_id)

        new_chapters: list[Chapter] = []

        for info in self.chapters_not_registered(
            manga.chapters_info, chapter_names_registered
        ):
            chapter = self.get_chapter(manga_url, info)
            new_chapters.append(chapter)

        if len(new_chapters) > 0:
            add_chapters(manga_id, new_chapters)

    def chapters_not_registered(
        self, chapters_info: list[ChapterInfo], chapter_names_registered: list[str]
    ) -> list[ChapterInfo]:
        informations = []

        for info in chapters_info:
            if not info.name in chapter_names_registered:
                informations.append(info)
        return informations

    def save(self, manga_url: str):
        """Save a new manga in the database."""
        manga = self.get_manga_with_chapter_pages(manga_url)
        add_manga(manga)

    @abstractmethod
    def get_manga_with_chapter_pages(self, manga_url: str) -> Manga:
        """Download a manga with chapter pages"""
        pass

    @abstractmethod
    def get_manga(self, manga_url: str) -> Manga:
        """Download a manga without chapter pages"""
        pass

    @abstractmethod
    def get_chapter(self, manga_url: str, info: ChapterInfo) -> Chapter:
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
