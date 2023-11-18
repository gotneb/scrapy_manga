# External packages
from bs4 import BeautifulSoup
from core.driver import get_driver_html, init_driver
# Ours code
from entities.chapter_info import ChapterInfo
from entities.manga import Manga
from requests import get

from .constants import origin
from .constants import language


def manga_detail(manga_url, show_window=False):
    """
    Visits the `manga_url` and extract all data on it.\n
    Arguments:\n
    `manga_url:` the manga content.
    `enable_gui:` show chrome window.
    """
    soup = BeautifulSoup(get(manga_url).content, "html.parser")

    title = _get_title(soup)
    alt_title = None
    status = _get_status(soup)
    author = _get_author(soup)
    artist = _get_artist(soup)
    score = _get_score(soup)
    thumbnail = _get_thumbnail(soup)
    genres = _get_genres(soup)
    summary = _get_summary(soup)
    chapters_info = _get_chapters(soup)

    return Manga(
        title=title,
        alternative_title=alt_title,
        author=author,
        artist=artist,
        status=status,
        url=manga_url,
        origin=origin,
        language=language,
        thumbnail=thumbnail,
        genres=genres,
        summary=summary,
        chapters_info=chapters_info,
        rating=score,
    )


def _get_title(soup: BeautifulSoup) -> str:
    """Returns manga's title."""
    tags = soup.css.select("div.post-title h1")
    title = tags[0].text
    title = title.strip()
    return title

def _get_status(soup: BeautifulSoup) -> str:
    """Returns manga's status."""
    tags = soup.css.select("div.post-status div.post-content_item")
    div = tags[1].css.select('div.summary-content')[0]
    status = div.text.strip()
    return status


def _get_author(soup: BeautifulSoup) -> str:
    """Returns manga's author."""
    tags = soup.css.select("div.post-content div.post-content_item")
    author = tags[3].css.select("div.summary-content")[0]
    author = author.text.strip()
    return author


def _get_artist(soup: BeautifulSoup) -> str:
    """Returns manga's author."""
    tags = soup.css.select("div.post-content div.post-content_item")
    artist = tags[4].css.select("div.summary-content")[0]
    artist = artist.text.strip()
    return artist


def _get_score(soup: BeautifulSoup) -> float:
    """Returns manga's author."""
    tags = soup.css.select("div.post-content div.post-rating span")
    score = tags[0].text.strip()
    score = float(score)
    return score


def _get_thumbnail(soup: BeautifulSoup) -> str:
    """Returns manga's thumbnail."""
    tags = soup.css.select("div.summary_image img.img-responsive")
    img = tags[0].get('src')
    img = img.strip()
    return img


def _get_genres(soup: BeautifulSoup) -> list[str]:
    """Returns manga's genres."""
    tags = soup.css.select("div.post-content div.post-content_item")
    a_tags = tags[5].css.select("a")
    genres = []
    for a in a_tags:
        genres.append(a.text)
    return genres

def _get_summary(soup: BeautifulSoup) -> str:
    """Returns manga's summary."""
    tags = soup.css.select("div.description-summary p")
    summary = tags[0].text.strip()
    return summary


def _get_chapters(soup: BeautifulSoup) -> list[ChapterInfo]:
    """Returns manga's chapters."""
    tags = soup.css.select("div.page-content-listing.single-page li a")
    chapters = []

    for li in tags:
        text = li.text.strip()
        if len(text) == 0:
            continue
        number = text.split(' ')[1] 
        chapters.append(ChapterInfo(number))
    return chapters