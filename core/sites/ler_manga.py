# Python
import math
from typing import Callable
# External packages
from bs4 import BeautifulSoup, Tag
from requests import get
from core.driver import init_driver
# Ours code
from entities.chapter_info import ChapterInfo
from entities.manga import Manga
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By

import time
import utils.debug_tools as utils

_domain = "https://lermanga.org"
_origin = "ler_manga"
_language = "portuguese"

LINKS_PER_PAGE = 100

# Helper function to `get_all_start_with`
def _link_start_with(link: str, letter: str) -> bool:
    name = link.split('/')[-2].lower()
    return name.startswith(letter)


# Helper functions to `get_all_start_with`
def _extract_link(tag: Tag) -> str:
    tags = tag.select('div.film-detail h3.film-name a')
    return tags[0].get('href')


def get_all_start_with(
    letter, show_window=False, on_link_received: Callable[[str], None] = None
) -> list[str]:
    """
    Visits `lermanga.org` and extract all links that starts with `letter` on its name.\n
    Arguments:
    `letter:` manga initial name.
    `show_window:` show google's chrome window.
    `on_link_received:` callback that's called when manga's link is received.\n
    Return:
    list of links.
    """
    if len(letter) > 2:
        raise Exception("letter must be an unique character.")
    if show_window:
        raise Exception("Couldn't open the window.")
    
    found_letter = False
    break_sequence = False
    index = 1
    url = ''

    links = []
    while True:
        if index == 1:
            url = f'{_domain}/mangas/?orderby=title&order=asc'
        else:
            url = f'{_domain}/mangas/page/{index}/?orderby=title&order=asc'
        
        req = get(url)
        soup = BeautifulSoup(req.content, "html.parser")
        tags = soup.css.select("div.film_list-wrap div.flw-item")

        for tag in tags:
            link = _extract_link(tag)
            if _link_start_with(link, letter):
                found_letter = True
                links.append(link)

                if on_link_received != None:
                    on_link_received(link)
            elif found_letter:
                break_sequence = True
        index += 1
        if found_letter and break_sequence:
            break

    return links


def get_populars(on_link_received: Callable[[str], None] = None) -> list[str]:
    """Visits the `lermanga.org` and returns most populars mangas right now."""
    URL = 'https://lermanga.org/mangas/?orderby=trending&order=desc'
    soup = BeautifulSoup(get(URL).content, "html.parser")
    anchor_tags = soup.css.select("div.film-detail a")
    links = []
    for a in anchor_tags:
        link = a.get('href')
        links.append(link)

        if on_link_received != None:
            on_link_received(link)
    return links


def get_latest_updates(
    limit: int = LINKS_PER_PAGE, on_link_received: Callable[[str], None] = None
) -> list[str]:
    """
    Returns a list of all links from `lermmanga.org` that were updateds.\n
    Arguments:
        `limit:` the total quantity of manga links will be extracted.
    Return:
        A list of recent mangas updated.
    """
    total_pages = math.ceil(limit / LINKS_PER_PAGE)
    counter = 0
    links = []

    for i in range(1, total_pages + 1):
        url = f'https://lermanga.org/capitulos/page/{i}/'
        if i == 1:
            url = 'https://lermanga.org/capitulos/'
        soup = BeautifulSoup(get(url).content, "html.parser")
        links_tags = soup.css.select("a.dynamic-visited")
        
        for a in links_tags:
            if counter == limit:
                break

            link = a.get('href')
            links.append(link)
            counter += 1

            if on_link_received != None:
                on_link_received(link)
    return links


# Helper function to get function `get_pages``
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

    ARBITRARY_NUMBER_ATTEMPTS = 20
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