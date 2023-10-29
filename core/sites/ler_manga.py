# Python
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

import time

_domain = "https://lermanga.org"
_origin = "ler_manga"
_language = "portuguese"


def _get_html(link) -> str:
    driver = init_driver(False)
    driver.set_page_load_timeout(10)

    driver.get(link)
    options = driver.find_elements(By.CSS_SELECTOR, 'div.nvs.slc select#slch option')
    options[-1].click()
    
    # Site might open a 2nd tab to show ads
    if len(driver.window_handles) == 2:
        # Close ADS tab
        driver.close()
        # Move to newly tab manga
        driver.switch_to.window(driver.window_handles[0])

    ARBITRARY_NUMBER_ATTEMPTS = 30
    ARBITRARY_SCROLL_AMOUNT = 700
    ARBITRARY_TIME = 0.05

    for _ in range(0, ARBITRARY_NUMBER_ATTEMPTS):
        ActionChains(driver)      \
        .scroll_by_amount(0, ARBITRARY_SCROLL_AMOUNT) \
        .perform()
        time.sleep(ARBITRARY_TIME)

    html = driver.page_source
    driver.close()
    return html


def get_pages(chapter_url: str) -> list[str]:
    """Extract all image links from a chapter.\n
    `chapter_url:` a chapter of a manga
    """
    soup = BeautifulSoup(_get_html(chapter_url), "html.parser")
    img_tags = soup.css.select("div.reader-area img")
    imgs = []
    for img in img_tags:
        imgs.append(img.get('src'))
    return imgs


def manga_detail(manga_url, show_window=False):
    """
    Visits the `manga_url` and extract all data on it.\n
    Arguments:\n
    `manga_url:` the manga content.
    `enable_gui:` show chrome window.
    """
    soup = BeautifulSoup(get(manga_url).content, "html.parser")

    title = get_title(soup)
    alt_title = None
    author = None
    artist = None
    score = get_score(soup)
    stt = None
    thumbnail = get_thumbnail(soup)
    genres = get_genres(soup)
    summary = get_summary(soup)
    chapters_info = get_chapters(soup)

    return Manga(
        title=title,
        alternative_title=alt_title,
        author=author,
        artist=artist,
        status=stt,
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
    tags = soup.css.select(
        "div.boxAnimeSobreLast h1 a")
    title = tags[0].text.replace('Ler Mangá', '')
    title = title.strip()
    return title


def get_score(soup: BeautifulSoup) -> int:
    """Returns manga's score."""
    tags = soup.css.select(
        "div.kk-star-ratings.kksr-template div.kksr-legend")
    score = tags[0].text.strip()
    score = score.split('/')[0]
    return float(score)


def get_thumbnail(soup: BeautifulSoup) -> str:
    """Returns manga's thumbnail."""
    tags = soup.css.select(
        "div.capaMangaInfo img")
    img = tags[0].get('src')
    return img


def get_genres(soup: BeautifulSoup) -> list[str]:
    """Returns manga's genres."""
    tags_list = soup.css.select(
        "div.anime div.boxAnimeSobreLast ul.genre-list.last-genre-series li a")
    genres = []
    for genre in tags_list:
        genres.append(genre.text.strip())
    return genres


def get_summary(soup: BeautifulSoup) -> str:
    """Returns manga's summary."""
    tags = soup.css.select(
        "div.boxAnimeSobreLast p")
    summary = tags[0].text
    summary = summary.replace('Sinopse: ', '').strip()
    return summary


def get_chapters(soup: BeautifulSoup) -> list[ChapterInfo]:
    """Returns all manga's chapters."""
    tags_chapters = soup.css.select("div.single-chapter a")
    chapters = []
    for chap in tags_chapters:
        c = chap            \
            .text           \
            .strip()        \
            .split(' ')[1]
        chapters.append(ChapterInfo(c))
    return chapters