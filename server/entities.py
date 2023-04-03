from dataclasses import dataclass


@dataclass
class Manga:
    """Class used to stored manga in the database"""

    title: str
    alternative_title: str
    author: str
    artist: str
    status: str
    url: str
    origin: str
    language: str
    total_chapters: int
    thumbnail: str
    genres: list[str]
    summary: str
    chapters_names: list[str]
    chapters: dict

    def to_dict(self):
        """Returns itself as a dictionary"""
        return self.__dict__

    @classmethod
    def dict_to_manga(cls, manga_dict: dict):
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
                total_chapters=manga_dict["total_chapters"],
                thumbnail=manga_dict["thumbnail"],
                genres=manga_dict["genres"],
                summary=manga_dict["summary"],
                chapters_names=manga_dict["chapters_names"],
                chapters=manga_dict["chapters"],
            )
        return None
