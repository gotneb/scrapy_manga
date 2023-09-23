from dataclasses import dataclass
from .entity import Entity
from .chapter import Chapter


class Manga(Entity):
    """Class used to stored manga in the database"""

    def __init__(
        self,
        title: str,
        alternative_title: str,
        author: str,
        artist: str,
        status: str,
        rating: float,
        url: str,
        origin: str,
        language: str,
        thumbnail: str,
        genres: list[str],
        summary: str,
        chapters: list[Chapter] = [],
    ) -> None:
        self.title: str = title
        self.alternative_title: str = alternative_title
        self.author: str = author
        self.artist: str = artist
        self.status: str = status
        self.rating: float = rating
        self.url: str = url
        self.origin: str = origin
        self.language: str = language
        self.thumbnail: str = thumbnail
        self.genres: list[str] = genres
        self.summary: str = summary
        self.chapters: list[Chapter] = chapters

    def chapters_to_dict_list(self):
        return list(map(lambda chapter: chapter.to_dict(), self.chapters))

    def get_chapter_names(self) -> list[str]:
        return list(map(lambda info: info.name, self.chapters))

    def filter_empty_chapters(self) -> None:
        results = []

        for chapter in self.chapters:
            if not chapter.is_empty():
                results.append(chapter)

        self.chapters = results

    def is_empty(self) -> bool:
        return len(self.chapters) == 0

    # Useful for debug
    def show(self) -> None:
        """Prints manga atributes on standard output"""
        print(
            f"""
            Origin: {self.origin}
            Url: {self.url}
            Title: {self.title}
            Alternative title: {self.alternative_title}
            Author: {self.author}
            Artist: {self.artist}
            Status: {self.status}
            Rating: {self.rating}
            Language: {self.language}
            Thumbnail: {self.thumbnail}
            genres: {self.genres}
            Summary: {self.summary}
            Chapters: {self.get_chapter_names()}
        """
        )

    def to_dict(self) -> dict:
        return {
            "title": self.title,
            "alternative_title": self.alternative_title,
            "author": self.author,
            "artist": self.artist,
            "status": self.status,
            "rating": self.rating,
            "url": self.url,
            "origin": self.origin,
            "language": self.language,
            "thumbnail": self.thumbnail,
            "genres": self.genres,
            "summary": self.summary,
            "chapters": self.chapters_to_dict_list(),
        }
