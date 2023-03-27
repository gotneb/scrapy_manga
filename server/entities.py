from dataclasses import dataclass


@dataclass
class Manga:
    """Class used to stored manga in the database"""

    title: str
    alternative_title: str
    author: str
    artist: str
    status: str
    origin: str
    language: str
    total_chapters: int
    thumbnail: str
    genres: list[str]
    summary: str
    chapters: dict

    def to_dict(self):
        """Returns itself as a dictionary"""
        return self.__dict__
