# External packages
from bs4 import BeautifulSoup, Tag
# Ours code
from entities.chapter_info import ChapterInfo
from entities.manga import Manga
from requests import get

from .constants import *


def manga_detail(manga_url, show_window=False):
    """
    Visits the `manga_url` and extract all data on it.\n
    Arguments:\n
    `manga_url:` the manga content.
    `enable_gui:` show chrome window.
    """
    manga_url = _sanitize_url(manga_url)
    soup = BeautifulSoup(get(manga_url).content, "html.parser")

    title = _get_title(soup)
    alt_title = _get_alt_title(soup)
    status = None
    author = _get_author(soup)
    artist = None
    score = None
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


# Needed to loads chapters names
def _sanitize_url(url: str) -> str:
    if 'waring' not in url:
        url = f'{url}?waring=1'
    return url


def _get_title(soup: BeautifulSoup) -> str:
    """Returns manga's title."""
    tags = soup.css.select("div.ttline h1")
    title = tags[0].text
    title = title.replace('Manga', '').strip()
    return title


def _get_alt_title(soup: BeautifulSoup) -> str | None:
    """Returns manga's alternative title."""
    tags = soup.css.select("div.bookintro ul.message li")
    for tag in tags:
        text = tag.text
        if 'Alternativa:' in text:
            text = text.replace('Alternativa:', '').strip()
            return text
    return None


def _get_author(soup: BeautifulSoup) -> str | None:
    """Returns manga's author."""
    tags = soup.css.select("div.bookintro ul.message li")
    for tag in tags:
        text = tag.text
        if 'Autor:' in text:
            text = text.replace('Autor:', '').strip()
            return text
    return None


def _get_thumbnail(soup: BeautifulSoup) -> str:
    """Returns manga's thumbnail."""
    tags = soup.css.select("div.bookintro a.bookface img")
    img = tags[0].get('src')
    return img


def _get_genres(soup: BeautifulSoup) -> list[str] | None:
    """Returns manga's genres."""
    tags = soup.css.select("div.bookintro ul.message li")
    for tag in tags:
        text = tag.text
        if 'Gênero:' in text:
            return _extract_genres(tag)
    return None


# Helper function to '_get_genres'
def _extract_genres(tag: Tag) -> list[str]:
    genres = []
    tags = tag.css.select('a')
    for a in tags:
        text = a.text
        text = text.lower().capitalize()
        genres.append(text)
    return genres


def _get_summary(soup: BeautifulSoup) -> str:
    """Returns manga's summary."""
    try:
        tags = soup.css.select("div.manga div.bookintro p")
        text = tags[0].text
        text = text.replace('Sinopse:', '').strip()
        return text
    except:
        return None


def _get_chapters(soup: BeautifulSoup) -> list[ChapterInfo]:
    """Returns manga's chapters."""
    tags = soup.css.select("a.chapter_list_a")
    chapters = []

    for a in tags:
        id = _get_chapter_id(a)
        text = a.text.strip()
        text = text.split(' ')[-1].strip()
        text = _sanitize(text)

        if _has_numbers(text):
            chapters.append(ChapterInfo(text, id))
        else:
            # Sometimes this site has a weird pattern on chapters names -.-'
            text = _find_number(a.text.strip())
            if text != None:
                chapters.append(ChapterInfo(text, id))

    return chapters


def _sanitize(value: str) -> str:
    if value.isdigit():
        return value.lstrip('0')
    return value


# Helper function to '_get_chapters'
def _get_chapter_id(tag: Tag) -> str:
    id = tag.get('href')
    id = id.split('/')[-1]
    id = id.split('.')[0]
    return id


# Helper function to '_get_chapters'
def _find_number(value: str) -> str | None:
    values = value.split(' ')
    for text in values:
        if _has_numbers(text):
            return text
    return None


# Helper function to '_get_chapters'
def _has_numbers(value: str) -> bool:
    return any(char.isdigit() for char in value)
