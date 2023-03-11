from dataclasses import dataclass


@dataclass
class Manga:
    """Mangas are objects that represent mangas avaliable either readm.org or mangalivre.net"""
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

    def to_dict(self):
        """Returns itself as a dictionary"""
        return {
            'title': self.title,
            'alternative_title': self.alternative_title,
            'author': self.author,
            'artist': self.artist,
            'thumbnail': self.thumbnail,
            'genres': self.genres,
            'summary': self.summary,
            'status': self.status,
            'total_chapters': self.total_chapters,
            'chapters': self.chapters
        }

    # Useful for debug
    def show(self) -> None:
        """Prints manga atributes on standard output"""
        print(f"""Title: {self.title}
Alternative title: {self.alternative_title}
Author: {self.author}\nArtist: {self.artist}
Status: {self.status}\nThumbnail: {self.thumbnail}
genres: {self.genres}\nSummary: {self.summary}
Total Chapters: {self.total_chapters}
Chapters: {self.chapters}""")
