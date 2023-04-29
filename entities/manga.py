from dataclasses import dataclass

from entities.chapter import Chapter


class Entity:
    def to_dict(self):
        """Returns itself as a dictionary"""
        return self.__dict__


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
    # Deprecated: Use `chapters_info` instead
    chapters: list[str]
    chapters_info: list[Chapter]

    def get_chapter_names(self):
        return self.chapters

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
Chapters: {self.chapters}""")