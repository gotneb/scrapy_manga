from dataclasses import dataclass


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
    url: str
    origin: str
    language: str
    thumbnail: str
    genres: list[str]
    summary: str
    chapters: dict

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


@dataclass
class WebsiteUpdate(Entity):
    origin: str
    populars: list[str]
    latest_updates: list[str]

    @classmethod
    def to_website_update(cls, update_dict: dict):
        if update_dict is not None:
            return WebsiteUpdate(
                origin=update_dict["origin"],
                populars=update_dict["populars"],
                latest_updates=update_dict["latest_updates"],
            )
        return None
