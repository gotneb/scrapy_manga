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
    total_chapters: int
    chapters: list[str]


    def show(self) -> None:
        print(f"Title: {self.title}\nAuthor: {self.author}\nStatus: {self.status}\nThumbnail: {self.thumbnail}\ngenres: {self.genres}\nSummary: {self.summary}\nTotal Chapters: {self.total_chapters}\nChapters: {self.chapters}")