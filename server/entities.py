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

    @classmethod
    def dict_to_manga(cls, manga_dict: dict):
        if manga_dict is not None:
            return Manga(
                manga_dict["title"],
                manga_dict["alternative_title"],
                manga_dict["author"],
                manga_dict["artist"],
                manga_dict["status"],
                manga_dict["origin"],
                manga_dict["language"],
                manga_dict["total_chapters"],
                manga_dict["thumbnail"],
                manga_dict["genres"],
                manga_dict["summary"],
                manga_dict["chapters"],
            )
        return None
