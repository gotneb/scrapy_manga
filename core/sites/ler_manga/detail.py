from bs4 import BeautifulSoup
from requests import get
from entities.chapter import Chapter

from entities.manga import Manga
from .constants import origin, language

def manga_detail(manga_url, show_window=False):
    """
    Visits the `manga_url` and extract all data on it.\n
    Arguments:\n
    `manga_url:` the manga content.
    `enable_gui:` show chrome window.
    """
    soup = BeautifulSoup(get(manga_url).content, "html.parser")

    # ===============================================
    # `Ler Manga` doesn't those kind of data -.-'
    # ===============================================
    alt_title = None
    author = None
    artist = None
    stt = None
    # ===============================================

    title = get_title(soup)
    score = get_score(soup)
    thumbnail = get_thumbnail(soup)
    genres = get_genres(soup)
    summary = get_summary(soup)
    chapters = get_chapters(soup)

    return Manga(
        title=title,
        alternative_title=alt_title,
        author=author,
        artist=artist,
        status=stt,
        url=manga_url,
        origin=origin,
        language=language,
        thumbnail=thumbnail,
        genres=genres,
        summary=summary,
        chapters=chapters,
        rating=score,
    )


def get_title(soup: BeautifulSoup) -> str:
    """Returns manga's title."""
    tags = soup.css.select("div.boxAnimeSobreLast h1 a")
    title = tags[0].text.replace("Ler Mangá", "")
    title = title.strip()
    return title


def get_score(soup: BeautifulSoup) -> int:
    """Returns manga's score."""
    tags = soup.css.select("div.kk-star-ratings.kksr-template div.kksr-legend")
    score = tags[0].text.strip()
    score = score.split("/")[0]
    return float(score)


def get_thumbnail(soup: BeautifulSoup) -> str:
    """Returns manga's thumbnail."""
    tags = soup.css.select("div.capaMangaInfo img")
    img = tags[0].get("src")
    return img


def get_genres(soup: BeautifulSoup) -> list[str]:
    """Returns manga's genres."""
    tags_list = soup.css.select(
        "div.anime div.boxAnimeSobreLast ul.genre-list.last-genre-series li a"
    )
    genres = []
    for genre in tags_list:
        genres.append(genre.text.strip())
    return genres


def get_summary(soup: BeautifulSoup) -> str:
    """Returns manga's summary."""
    tags = soup.css.select("div.boxAnimeSobreLast p")
    summary = tags[0].text
    summary = summary.replace("Sinopse: ", "").strip()
    return summary


def get_chapters(soup: BeautifulSoup) -> list[Chapter]:
    """Returns all manga's chapters."""
    tags_chapters = soup.css.select("div.single-chapter a")
    chapters = []
    for chap in tags_chapters:
        c = chap.text.strip().split(" ")[1]
        chapters.append(Chapter(c))
    return chapters
