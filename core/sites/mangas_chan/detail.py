# External packages
from bs4 import BeautifulSoup
from core.driver import get_driver_html, init_driver
# Ours code
from entities.chapter_info import ChapterInfo
from entities.manga import Manga

from .constants import origin
from .constants import language


def manga_detail(manga_url, show_window=False):
    """
    Visits the `manga_url` and extract all data on it.\n
    Arguments:\n
    `manga_url:` the manga content.
    `enable_gui:` show chrome window.
    """
    driver = init_driver(True)
    soup = BeautifulSoup(get_driver_html(driver, manga_url), "html.parser")

    title = _get_title(soup)
    alt_title = _get_alt_title(soup)
    status, author, artist = _get_status_author_artist(soup)
    score = _get_score(soup)
    thumbnail = _get_thumbnail(soup)
    genres = _get_genres(soup)
    summary = _get_summary(soup)
    chapters_info = _get_chapters(soup)

    driver.quit()

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
    tags = soup.css.select("div#titlemove h1.entry-title")
    title = tags[0].text
    title = title.strip()
    return title


def _get_alt_title(soup: BeautifulSoup) -> str:
    """Returns manga's alternative title."""
    try:
        tags = soup.css.select("div#titlemove span.alternative")
        alt_title = tags[0].text
        alt_title = alt_title.strip()
        return alt_title
    except:
        return ""


def _get_status_author_artist(soup: BeautifulSoup) -> (str, str, str):
    """Returns manga's status, author and artist. In that order."""
    status, author, artist = "", "", ""
    try:
        tags = soup.css.select("div.tsinfo.bixbox div.imptdt")
        for tag in tags:
            if "Status" in tag.text:
                status = tag.css.select('i')[0].text
            elif "Autor" in tag.text:
                author = tag.css.select('i')[0].text
            elif "Artista" in tag.text:
                artist = tag.css.select('i')[0].text
        return status, author, artist
    except:
        return status, author, artist


def _get_score(soup: BeautifulSoup) -> float:
    """Returns manga's score."""
    try:
        tags = soup.css.select("div.rating-prc div.num")
        score = tags[0].text.strip()
        return float(score)
    except:
        return 0


def _get_thumbnail(soup: BeautifulSoup) -> str:
    """Returns manga's thumbnail."""
    try:
        tags = soup.css.select('img.attachment-.size-.wp-post-image')
        thumbnail = tags[0].get('src')
        return thumbnail
    except:
        return ""


def _get_genres(soup: BeautifulSoup) -> str:
    """Returns manga's genres."""
    tags = soup.css.select("div.wd-full span.mgen a")
    genres = []
    for a in tags:
        genres.append(a.text)
    return genres


def _get_summary(soup: BeautifulSoup) -> str:
    """Returns manga's summary."""
    tags = soup.css.select("div.info-desc.bixbox div.wd-full div.entry-content.entry-content-single")
    summary = tags[0].text.strip()
    return summary


def _get_chapters(soup: BeautifulSoup) -> list[ChapterInfo]:
    """Returns manga's chapters."""
    tags = soup.css.select("ul.clstyle li")
    chapters = []
    for li in tags:
        number = li.get('data-num')
        chapters.append(ChapterInfo(number))
    return chapters