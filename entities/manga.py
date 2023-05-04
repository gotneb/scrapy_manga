# Python
from dataclasses import dataclass
# Entities
from entities.chapter import Chapter


@dataclass
class Manga():
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
    chapters_info: list[Chapter]

    def get_chapter_names(self) -> list[str]:
        values = []
        # Not sure if it's the best way to return chapter's value
        for c in self.chapters_info:
            values.append(c.number)
        return values

    def to_dict(self):
        return {
            'title': self.title,
            'alternative': self.alternative_title,
            'author': self.author,
            'artist': self.artist,
            'url': self.url,
            'origin': self.origin,
            'language': self.language,
            'thumbnail': self.thumbnail,
            'genres': self.genres,
            'summary': self.summary,
            'chapters': self.chapters_info
        }

    @classmethod
    def to_manga(cls, manga_dict: dict):
        if manga_dict is not None:
            return Manga(
                title=manga_dict["title"],
                alternative_title=manga_dict["alternative_title"],
                author=manga_dict["author"],
                artist=manga_dict["artist"],
                status=manga_dict["status"],
                url=manga_dict["url"],
                origin=manga_dict["origin"],
                language=manga_dict["language"],
                thumbnail=manga_dict["thumbnail"],
                genres=manga_dict["genres"],
                summary=manga_dict["summary"],
                chapters=manga_dict["chapters"],
            )
        return None

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
Chapters: {self.get_chapter_names()}""")
