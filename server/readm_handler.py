from core.manga import Manga as MangaDetails
from .entities import Manga
from core.sites.readm import (
    manga_detail as get_manga_details,
    get_pages,
    get_all_start_with,
)
from .database import MangaDatabase
from time import time


class ReadmHandler:
    def __init__(self, database: MangaDatabase) -> None:
        self.database = database
        self.total_time = 0
        self.total_iterations = 0

    def start(self):
        self.total_time = 0
        self.total_iterations = 0

        print(
            "----------------------  Starting Database Handler System ----------------------\n",
        )
        initial_time = time()

        letters = [chr(i) for i in range(97, 123)]

        for letter in letters:
            get_all_start_with(letter, False, self._perform)

        final_time = time()

        print(
            ":: --- Total Duration: {:.2f} s.".format(final_time - initial_time),
            end="\n",
        )

    def _perform(self, manga_url: str):
        initial_time = time()

        if not self.database.exists_by_url(manga_url):
            print(f"Storing manga with url '{manga_url}' for the first time.")
            self._save_manga(manga_url)

        else:
            print(f"Updating manga with url '{manga_url}.'")
            self._update_manga(manga_url)

        final_time = time()

        self._report(initial_time, final_time)

    def _update_manga(self, manga_url: str):
        try:
            current_manga = self.database.get_by_url(manga_url)
            details = get_manga_details(manga_url, False)

            for chapter_name in details.chapters:
                if not chapter_name in current_manga.chapters_names:
                    new_chapter = self._get_chapter(manga_url, chapter_name)
                    current_manga.chapters.update(new_chapter)
                    current_manga.total_chapters += 1
                    current_manga.chapters_names.append(chapter_name)
        except Exception as error:
            print(error)

    def _save_manga(self, manga_url):
        try:
            manga = self._get_manga(manga_url)
            self.database.add(manga)
        except Exception as error:
            print(error)

    def _get_manga(self, manga_url: str) -> Manga:
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
        cp_url = f"{manga_url}/{chapter_name}/all-pages"
        pages = get_pages(cp_url)
        return {chapter_name: pages}

    def _report(self, initial_time: float, final_time: float):
        total_time = final_time - initial_time
        print("     => Operation duration: {:.2f} s. \n".format(total_time))

        self.total_iterations += 1
        self.total_time += total_time

        print(
            ":: --- Average time of operations: {:.2f} s \n".format(
                self.total_time / self.total_iterations
            )
        )
