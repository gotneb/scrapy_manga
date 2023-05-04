from dataclasses import dataclass
from .entity import Entity
from .chapter import Chapter
from .chapter_info import ChapterInfo


@dataclass
class Manga(Entity):
    """Class used to stored manga in the database"""

    title: str
    alternative_title: str
    author: str
    artist: str
    status: str
    rating: float
    url: str
    origin: str
    language: str
    thumbnail: str
    genres: list[str]
    summary: str
    chapters_info: list[ChapterInfo] | None
    chapters: list[Chapter] | None = None

    def get_chapter_names(self) -> list[str]:
        values = []
        # Not sure if it's the best way to return chapter's value
        for c in self.chapters_info:
            values.append(c.name)
        return values

    def chapters_to_dict_list(self):
        if self.chapters:
            return list(map(lambda chapter: chapter.to_dict(), self.chapters))
        else:
            return []

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

    def get_chapter_names(self) -> list[str]:
        return list(map(lambda info: info.name, self.chapters_info))

    # Useful for debug
    def show(self) -> None:
        """Prints manga atributes on standard output"""
        print(
            f"""Origin: {self.origin}
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
                Chapters: {self.get_chapter_names()}"""
        )
