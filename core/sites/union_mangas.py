# Python
import math
from typing import Callable
# External packages
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
# Ours code
from core.driver import init_driver
from entities.chapter_info import ChapterInfo
from entities.manga import Manga


def get_all_start_with(
    letter, show_window=False, on_link_received: Callable[[str], None] = None
) -> list[str]:
    """
    Visits `unionleitor.top` and extract all links that starts with `letter` on its name.

    Arguments:

    `letter:` manga initial name.

    `show_window:` show google's chrome window.

    `on_link_received:` callback that's called when manga's link is received.
    """
    if len(letter) > 2:
        raise Exception("letter must be an unique character.")

    url = f'https://unionleitor.top/lista-mangas/a-z/1/{letter}'
    driver = init_driver(False)
    driver.get(url)
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")

    # Get the button to skip to the last page in that section
    last = soup.css.select("div.row div.col-md-8.tamanho-bloco-perfil div.row.text-center nav li a")[-1]
    # Extract url and actually get the last index
    end_index = int(last['href'].split('/')[-2])
    
    links = []
    for index in range(1, end_index + 1):
        driver.get(f'https://unionleitor.top/lista-mangas/a-z/{index}/{letter}')
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")

        # Extract links from mangas
        tags = soup.css.select('div.row div.col-md-8.tamanho-bloco-perfil div.row div.col-md-3.col-xs-4.text-center.lista-mangas-novos a')
        for t in tags:
            if t.has_attr('class'):
                l = t['href']
                links.append(l)
                # Callback
                if on_link_received != None:
                    on_link_received(l)

    driver.quit()
    return links


def manga_detail(manga_url, show_window=False):
    """
    Visits the `manga_url` and extract all data on it.\n
    Arguments:\n
    `manga_url:` the manga content. Must have `readm.org` or `mangalivre.net` domain.
    `enable_gui:` show chrome window.
    """
    if show_window:
        print('WARNING: "show_window" is disable...')
    
    # `Union Manga` returns a 403 code when acessing it trough `requests`
    # The solution is (sadly) emulate a browser (slow...) to fake a real person
    driver = init_driver(False)
    driver.get(manga_url)
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")

    # Clean resources
    driver.quit()

    title = get_title(soup)
    alt_title = get_alt_title(soup)
    author = get_author(soup)
    artist = get_artist(soup)
    score = get_score(soup)
    stt = get_status(soup)
    genres = get_genres(soup)
    summary = get_summary(soup)
    thumbnail = get_thumbnail(soup)
    chapters_info = get_chapters(soup)

    return Manga(
        title=title,
        alternative_title=alt_title,
        author=author,
        artist=artist,
        status=stt,
        url=manga_url,
        origin='union_mangas',
        language='portuguese',
        thumbnail=thumbnail,
        genres=genres,
        summary=summary,
        chapters_info=chapters_info,
        rating=score,
    )


def get_title(soup: BeautifulSoup) -> str:
    """Returns title from manga"""
    h2 = soup.css.select("div.col-md-8.perfil-manga div.col-md-12 h2")
    return h2[0].string


def get_alt_title(soup: BeautifulSoup) -> str:
    """Returns alternative title from manga. Otherwise None."""
    try:
        title = soup.css.select("div.col-md-8.col-xs-12 h4.media-heading.manga-perfil")
        # It removes 'Titulos Altenativo(s)'
        return title[0].text.split(':')[1].strip()
    except:
        return None
    

def get_author(soup: BeautifulSoup) -> str:
    """Returns author from manga. Otherwise None."""
    try:
        title = soup.css.select("div.col-md-8.col-xs-12 h4.media-heading.manga-perfil")
        # It removes 'Autor'
        return title[2].text.split(':')[1].strip()
    except:
        return None


def get_artist(soup: BeautifulSoup) -> str:
    """Returns author from manga. Otherwise None."""
    try:
        title = soup.css.select("div.col-md-8.col-xs-12 h4.media-heading.manga-perfil")
        # It removes 'Artista'
        return title[3].text.split(':')[1].strip()
    except:
        return None


def get_score(soup: BeautifulSoup) -> float:
    """Returns the score given by the users."""
    # It removes 'votos' word
    score = soup.css.select("div.col-md-8.col-xs-12 h2")
    score = score[0].text.split(' ')[0]
    return float(score.removeprefix('#'))


def get_status(soup: BeautifulSoup) -> str:
    """Returns status from manga. Otherwise None."""
    try:
        title = soup.css.select("div.col-md-8.col-xs-12 h4.media-heading.manga-perfil")
        # It removes 'Status' word
        return title[4].text.split(':')[1].strip()
    except:
        return None
    

def get_genres(soup: BeautifulSoup) -> list[str]:
    """Returns a list of genres from manga. Otherwise None."""
    try:
        tag = soup.css.select("div.col-md-8.col-xs-12 h4.media-heading.manga-perfil")
        # It removes 'Genêro(s)' word
        raw = tag[1].text.split(':')[1].strip()
        # Format genres
        genres = raw.replace(',', '').split(' ')
        return genres
    except:
        return None
    

def get_summary(soup: BeautifulSoup) -> str:
    """Returns summary from manga."""
    elems = soup.css.select("div.col-md-8.col-xs-12 div.panel.panel-default")
    return elems[0].text.strip()


def get_thumbnail(soup: BeautifulSoup) -> str:
    """Returns thumbnail (cover) from manga."""
    elems = soup.css.select("img.img-thumbnail")
    return elems[0]['src']


def get_chapters(soup: BeautifulSoup) -> list[ChapterInfo]:
    """Returns a list of chapters from manga."""
    elems = soup.css.select("div.row.capitulos div.col-xs-6.col-md-6 a")
    chapters = []
    for e in elems:
        if "Cap." in e.text:
            c = e.text.split(' ')[1]
            chapters.append(ChapterInfo(name=c))
    return chapters