from dataclasses import dataclass

@dataclass
class Manga:
    """Class represent a manga hosted in readm.org"""
    title: str
    author: str
    thumbnail: str
    genres: list[str]
    summary: str
    status: str
    chapters: list[str]
    total_chapters: int

    def __init__(self, title, author, thumbnail, genres, summary, status, chapters, total_chapters):
        self.title = title
        self.author = author
        self.thumbnail = thumbnail
        self.genres = genres
        self.summary = summary
        self.status = status
        self.chapters = chapters
        self.total_chapters = total_chapters
