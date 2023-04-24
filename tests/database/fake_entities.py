from server import Manga


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


def get_fake_manga_list(total: int = 3, origin: str = "readm") -> list[Manga]:
    mangas = []

    for i in range(total):
        manga = Manga(
            title=f"title{i}",
            alternative_title=f"alternative_title{i}",
            author=f"author{i}",
            artist=f"artist{i}",
            status=f"status{i}",
            url=f"url{i}",
            origin=origin,
            language="english",
            thumbnail=f"thumb_url{i}",
            genres=["genre1", "genre2"],
            summary=f"summary{i}",
            chapters={"1": ["page1", "page2"], "2c": ["page1", "page2"]},
        )

        mangas.append(manga)
    return mangas
