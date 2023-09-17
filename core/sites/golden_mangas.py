# Python
import math
from typing import Callable

# External packages
from bs4 import BeautifulSoup
from requests import get

# Ours code
from core.driver import init_driver
from entities.chapter_info import ChapterInfo
from entities.manga import Manga


_domain = "https://www.goldenmangas.top"
_origin = "golden_mangas"
_language = "portuguese"


def _get_html(link) -> str:
    driver = init_driver(False)
    driver.set_page_load_timeout(4)

    try:
        driver.get(link)
    except:
        driver.execute_script("window.stop();")

    html = driver.page_source
    driver.close()
    return html


def get_pages(chapter_url) -> list[str]:
    """Extract all image links from a manga chapter.

    `chapter_url:` a chapter of a manga
    """
    soup = BeautifulSoup(_get_html(chapter_url), "html.parser")
    url_imgs = []

    tags = soup.css.select(
        "body article div div#leitor article.container.backTop div#leitor_full.row div#capitulos_images.col-sm-12.text-center img.img-responsive.img-manga"
    )
    for t in tags:
        img = f"{_domain}{t['src']}"
        url_imgs.append(img)

    return url_imgs


def get_latest_updates(
    limit: int = 18, on_link_received: Callable[[str], None] = None
) -> list[str]:
    """
    Returns a list of all links from `goldenmangas.top` that were updateds.\n
    Arguments:
        `limit:` the total quantity of manga links will be extracted.
    Return:
        A list of recent mangas updated.
    """
    # 540 it's equivalente to 30 page on "goldenmangas.top".
    if limit > 540:
        raise Exception("limit must be lower or equals than 540!")

    total_pages = math.ceil(limit / 18)
    counter = 0
    links = []

    for i in range(1, total_pages + 1):
        if counter == limit:
            break

        html = _get_html(f"{_domain}/index.php?pagina={i}")
        soup = BeautifulSoup(html, "html.parser")
        tags = soup.css.select(
            "div.container div.row div.col-sm-8.col-xs-12 div#response.row div.col-sm-12.atualizacao div.row > a"
        )

        for a in tags:
            if counter == limit:
                break

            l = f"{_domain}{a['href']}"
            links.append(l)
            counter += 1

            if on_link_received != None:
                on_link_received(l)

    return links


def get_all_start_with(
    letter: str, show_window=False, on_link_received: Callable[[str], None] = None
) -> list[str]:
    """
    Visits `goldenmanga.top` and extract all links that starts with `letter` on its name.\n
    Arguments:
    `letter:` manga initial name.
    `show_window:` show google's chrome window.
    `on_link_received:` callback that's called when manga's link is received.\n
    Return:
    list of links.
    """
    if len(letter) > 2:
        raise Exception("letter must be an unique character.")
    letter = letter.upper()

    if show_window:
        raise Exception('"show_window" is disabled...')

    url_page = f"{_domain}/mangabr?letra={letter.upper()}&pagina=1"
    soup = BeautifulSoup(_get_html(url_page), "html.parser")

    # Get last index value
    tags = soup.css.select(
        "div.container.text-center nav.text-center ul.pagination li a"
    )
    if len(tags) > 3:
        end_index = int(tags[-2].text)
    else:
        end_index = 1

    # Get data on manga
    links = []
    for i in range(1, end_index + 1):
        # if it's the first, then it isn't needed to load the content again...
        if i != 1:
            url_page = f"{_domain}/mangabr?letra={letter}&pagina={i}"
            soup = BeautifulSoup(_get_html(url_page), "html.parser")

        # Get manga content
        tags = soup.css.select(
            "div.container section.row div.mangas.col-lg-2.col-md-2.col-xs-6 a"
        )
        for a in tags:
            l = f'{_domain}{a["href"]}'
            links.append(l)
            # Callback
            if on_link_received != None:
                on_link_received(l)

    return links


def get_populars(on_link_received: Callable[[str], None] = None) -> list[str]:
    """Visits the `goldenmanga.top` and returns top 20 most populars mangas."""
    soup = BeautifulSoup(_get_html(_domain), "html.parser")
    tags = soup.css.select(
        "div.container div.row div.col-sm-4.col-xs-12 section#capitulosdestaque.hidden-xs a"
    )
    populars = []
    for a in tags:
        link = f'{_domain}{a["href"]}'
        # Remove the chapter number from link
        split_link = link.split("/")[0:-1]
        # Now it's only the manga link itself
        manga_link = "/".join(split_link)
        populars.append(manga_link)
        #  Callback
        if on_link_received != None:
            on_link_received(manga_link)

    return populars


def manga_detail(manga_url, show_window=False) -> Manga:
    """
    Visits the `manga_url` and extract all data on it.\n
    Arguments:\n
    `manga_url:` the manga content. Must have `readm.org` or `mangalivre.net` domain.
    `enable_gui:` show chrome window.
    """
    soup = BeautifulSoup(_get_html(manga_url), "html.parser")

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
        origin=_origin,
        language=_language,
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
    tag = soup.css.select(
        "div.container.manga div.row div.col-sm-8 div.row div.col-sm-4.text-right img.img-responsive"
    )
    img = tag[0]["src"]
    return f"{_domain}{img}"


def get_genres(soup: BeautifulSoup) -> list[str]:
    """Returns a list of genres from manga."""
    tags = soup.css.select(
        "div.container.manga div.row div.col-sm-8 h5.cg_color a.label.label-warning"
    )
    genres = []
    for g in tags:
        if len(g.text) > 0:
            genres.append(g.text)
    return genres


def get_score(soup: BeautifulSoup) -> float:
    """Returns the score given by the users."""
    try:
        tag = soup.css.select("div.container.manga div.row div.col-sm-8 h2.cg_color")[1]
        score = tag.text.split(" ")[0].replace("#", "")
        return float(score)
    except:
        # There's no score at all
        return None


def get_summary(soup: BeautifulSoup) -> str:
    """Returns summary from manga."""
    tag = soup.css.select(
        "div.container.manga div.row div.col-sm-8 div#manga_capitulo_descricao"
    )[0]
    return " ".join(tag.text.split())


def get_chapters(soup: BeautifulSoup) -> list[ChapterInfo]:
    """Returns a list of chapters from manga."""
    a_tags = soup.css.select(
        "div.container.manga div.row div.col-sm-8 ul#capitulos.capitulos li.row a div.col-sm-5"
    )

    chapters = []
    for a in a_tags:
        text = a.text.strip().split(" ")
        if "Cap" in text:
            chapters.append(ChapterInfo(text[1]))

    return chapters
