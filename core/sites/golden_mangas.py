from bs4 import BeautifulSoup
from requests import get

from entities.chapter_info import ChapterInfo
from entities.manga import Manga

_domain = 'https://goldenmangas.top'

def manga_detail(manga_url, show_window=False) -> Manga:
    """
    Visits the `manga_url` and extract all data on it.\n
    Arguments:\n
    `manga_url:` the manga content. Must have `readm.org` or `mangalivre.net` domain.
    `enable_gui:` show chrome window.
    """
    if show_window:
        raise Exception('"show_window" is disabled...')
    
    html = get(manga_url)
    soup = BeautifulSoup(html.text, "html.parser")

    title = get_title(soup)
    alt_title = None
    author = get_author(soup)
    artist = get_artist(soup)
    score = get_score(soup)
    stt = get_status(soup)
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
        origin='golden_manga',
        language='portuguese',
        thumbnail=thumbnail,
        genres=genres,
        summary=summary,
        chapters_info=chapters_info,
        rating=score,
    )


def get_title(soup: BeautifulSoup) -> str:
    """Returns title from manga"""
    h2 = soup.css.select("div.container.manga div.row div.col-sm-8 h2.cg_color")
    return h2[0].text


def get_author(soup: BeautifulSoup) -> str:
    """Returns author from manga."""
    tag = soup.css.select("div.container.manga div.row div.col-sm-8 h5.cg_color a")
    author = tag[-3].text.strip()
    return author


def get_artist(soup: BeautifulSoup) -> str:
    """Returns author from manga."""
    tag = soup.css.select("div.container.manga div.row div.col-sm-8 h5.cg_color a")
    text = tag[-2].text.strip()
    return text


def get_status(soup: BeautifulSoup) -> str:
    """Returns status from manga."""
    tag = soup.css.select("div.container.manga div.row div.col-sm-8 h5.cg_color a")
    text = tag[-1].text.strip()
    return text


def get_thumbnail(soup: BeautifulSoup) -> str:
    """Returns thumbnail (image) from manga."""
    tag = soup.css.select("div.container.manga div.row div.col-sm-8 div.row div.col-sm-4.text-right img.img-responsive")
    img = tag[0]['src']
    return f'{_domain}{img}'


def get_genres(soup: BeautifulSoup) -> list[str]:
    """Returns a list of genres from manga."""
    tags = soup.css.select("div.container.manga div.row div.col-sm-8 h5.cg_color a.label.label-warning")
    genres = []
    for g in tags:
        if len(g.text) > 0:
            genres.append(g.text)
    return genres


def get_score(soup: BeautifulSoup) -> float:
    """Returns the score given by the users."""
    try:
        tag = soup.css.select("div.container.manga div.row div.col-sm-8 h2.cg_color")[1]
        score = tag.text.split(' ')[0].replace('#', '')
        return float(score)
    except:
        # There's no score at all
        return None


def get_summary(soup: BeautifulSoup) -> str:
    """Returns summary from manga."""
    tag = soup.css.select("div.container.manga div.row div.col-sm-8 div#manga_capitulo_descricao")[0]
    return " ".join(tag.text.split())


def get_chapters(soup: BeautifulSoup) -> list[ChapterInfo]:
    """Returns a list of chapters from manga."""
    a_tags = soup.css.select(
        "div.container.manga div.row div.col-sm-8 ul#capitulos.capitulos li.row a div.col-sm-5"
    )

    chapters = []
    for a in a_tags:
        text = a.text.strip().split(' ')
        if "Cap" in text:
            chapters.append(ChapterInfo(text[1]))
    
    return chapters