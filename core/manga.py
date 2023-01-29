from dataclasses import dataclass

@dataclass
class Manga:
    """Class represent a manga hosted in readm.org"""
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


    def show(self) -> None:
        """Prints manga atributes on standard output"""
        print(f"""Title: {self.title}
Alternative title: {self.alternative_title}
Author: {self.author}\nArtist: {self.artist}
Status: {self.status}\nThumbnail: {self.thumbnail}
genres: {self.genres}\nSummary: {self.summary}
Total Chapters: {self.total_chapters}
Chapters: {self.chapters}""")