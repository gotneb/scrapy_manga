# Python
from typing import Callable
# External packages
from bs4 import BeautifulSoup
# Ours code
from core.driver import init_driver
from entities.chapter_info import ChapterInfo
from entities.manga import Manga


def get_pages(chapter_url) -> list[str]:
    """Extract all image links from a manga chapter.

    `manga_url:` a chapter of a manga
    """
    driver = init_driver(False)
    driver.get(chapter_url)
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")

    driver.quit()

    tag_pages = soup.css.select("img.img-responsive.img-manga")
    pages = []
    for page in tag_pages:
        pages.append(page['src'])

    return pages


def get_populars(on_link_received: Callable[[str], None] = None) -> list[str]:
    """Visits the `unionleitor.top` and returns top 12 most populars mangas."""
    populars_url = 'https://unionleitor.top/home' 
    driver = init_driver(False)
    driver.get(populars_url)
    html = driver.page_source
    driver.quit()
    soup = BeautifulSoup(html, "html.parser")

    elems = soup.css.select("div.row")[4]
    links = []
    for e in elems:
        a_tag = e.find('a')
        # Wtf, I really don't even know why -1 is happening...
        if a_tag != None and a_tag != -1:
            link = a_tag['href']
            links.append(link)
            # Callback
            if on_link_received != None:
                on_link_received(link)

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