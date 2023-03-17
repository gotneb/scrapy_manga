from dataclasses import dataclass


@dataclass
class MangaDetailsEntity:
    """Class used to stored manga manga_details in the database"""

    title: str
    alternative_title: str
    author: str
    artist: str
    thumbnail: str
    genres: list[str]
    summary: str
    status: str
    total_chapters: int
    chapters: list[str]
    origin: str
    id: str = None

    def to_dict(self):
        """Returns itself as a dictionary"""
        return {
            "title": self.title,
            "alternative_title": self.alternative_title,
            "author": self.author,
            "artist": self.artist,
            "thumbnail": self.thumbnail,
            "genres": self.genres,
            "summary": self.summary,
            "status": self.status,
            "total_chapters": self.total_chapters,
            "chapters": self.chapters,
            "origin": self.origin,
        }


@dataclass
class ChapterEntity:
    """Class used to stored manga chapter in the database"""

    manga_id: str
    chapter_num: str
    image_urls: list[str]

    def to_dict(self) -> dict:
        return {
            "manga_id": self.manga_id,
            "chapter_num": self.chapter_num,
            "image_urls": self.image_urls,
        }
