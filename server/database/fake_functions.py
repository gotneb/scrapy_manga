from .entities import Manga


def get_fake_manga(origin: str = "readm") -> Manga:
    """Retorns a fake Manga object."""
    manga = Manga(
        title="title",
        alternative_title="alternative_title",
        author="author",
        artist="artist",
        status="status",
        url="url",
        origin=origin,
        language="english",
        thumbnail="thumb_url",
        genres=["genre1", "genre2"],
        summary="summary",
        chapters={"1": ["page1", "page2"], "2c": ["page1", "page2"]},
    )
    return manga
