"""Class used to stored manga chapter in the database"""

class ChapterEntity:
    def __init__(self, manga_id: str, chapter_num: str, image_urls: list[str]) -> None:
        self.manga_id = manga_id
        self.chapter_num = chapter_num
        self.image_urls = image_urls
    
    def to_dict(self) -> dict:
        return {
            'manga_id': self.manga_id,
            'chapter_num': self.chapter_num,
            'image_urls': self.image_urls
        }