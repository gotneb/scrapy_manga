# Python
import math
from typing import Callable
# External packages
from bs4 import BeautifulSoup
from requests import get
from core.driver import init_driver
# Ours code
from entities.chapter_info import ChapterInfo
from entities.manga import Manga
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By

import utils.debug_tools as utils

_domain = "https://mangaschan.net"
_origin = "mangas_chan"
_language = "portuguese"

_default_thumbnail_not_found = 'https://img.freepik.com/vetores-gratis/erro-404-com-ilustracao-do-conceito-de-paisagem_114360-7898.jpg?size=626&ext=jpg&ga=GA1.1.1413502914.1696809600&semt=ais'


def manga_detail(manga_url, show_window=False):
    """
    Visits the `manga_url` and extract all data on it.\n
    Arguments:\n
    `manga_url:` the manga content.
    `enable_gui:` show chrome window.
    """
    soup = BeautifulSoup(get(manga_url).content, "html.parser")
    #soup = BeautifulSoup(utils.read_file('mangas_chan_berserk.txt'), "html.parser")

    title = get_title(soup)
    alt_title = get_alt_title(soup)
    status, author, artist = get_status_author_artist(soup)
    score = get_score(soup)
    thumbnail = get_thumbnail(soup)
    genres = get_genres(soup)
    summary = get_summary(soup)
    chapters_info = get_chapters(soup)

    return Manga(
        title=title,
        alternative_title=alt_title,
        author=author,
        artist=artist,
        status=status,
        url=manga_url,
        origin=_origin,
        language=_language,
        thumbnail=thumbnail,
        genres=genres,
        summary=summary,
        chapters_info=chapters_info,
        rating=score,
    )


def get_title(soup: BeautifulSoup) -> str:
    """Returns manga's title."""
    tags = soup.css.select("div#titlemove h1.entry-title")
    title = tags[0].text
    title = title.strip()
    return title


def get_alt_title(soup: BeautifulSoup) -> str:
    """Returns manga's alternative title."""
    try:
        tags = soup.css.select("div#titlemove span.alternative")
        alt_title = tags[0].text
        alt_title = alt_title.strip()
        return alt_title
    except:
        return ""


def get_status_author_artist(soup: BeautifulSoup) -> (str, str, str):
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


def get_score(soup: BeautifulSoup) -> float:
    """Returns manga's score."""
    try:
        tags = soup.css.select("div.rating-prc div.num")
        score = tags[0].text.strip()
        return float(score)
    except:
        return 0


def get_thumbnail(soup: BeautifulSoup) -> str:
    """Returns manga's thumbnail."""
    try:
        tags = soup.css.select('img.attachment-.size-.wp-post-image')
        thumbnail = tags[0].get('src')
        return thumbnail
    except:
        return ""


def get_genres(soup: BeautifulSoup) -> str:
    """Returns manga's genres."""
    tags = soup.css.select("div.wd-full span.mgen a")
    genres = []
    for a in tags:
        genres.append(a.text)
    return genres


def get_summary(soup: BeautifulSoup) -> str:
    """Returns manga's summary."""
    tags = soup.css.select("div.info-desc.bixbox div.wd-full div.entry-content.entry-content-single")
    summary = tags[0].text.strip()
    return summary


def get_chapters(soup: BeautifulSoup) -> list[ChapterInfo]:
    """Returns manga's chapters."""
    tags = soup.css.select("ul.clstyle li")
    chapters = []
    for li in tags:
        number = li.get('data-num')
        chapters.append(ChapterInfo(number))
    return chapters