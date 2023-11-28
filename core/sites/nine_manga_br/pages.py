# External packages
from bs4 import BeautifulSoup
# Ours code
from requests import get

from core.driver import *
from .constants import *

UNDEFINED = 50

def get_pages(manga_url) -> list[str]:
    """Extract all image links from a manga chapter.

    `manga_url`: a manga's chapter
    """
    if domain not in manga_url:
        raise Exception("get pages fucntion doesn't support this site!")

    driver = init_driver(False)
    pages = []
    total = -1

    for index in range(1, UNDEFINED):
        url = _to_index(manga_url, index)
        soup = BeautifulSoup(get_driver_html(driver, url), "html.parser")
        _extract_individual_page(soup, pages)

        if index == 1:
            total = _get_total_indexes(soup)
        if index >= total:
            break

    driver.close()
    return pages


def _extract_individual_page(soup: BeautifulSoup, pages: list[str]) -> None:
    tags = soup.css.select("img.manga_pic")
    for img in tags:
        pages.append(img.get('src'))


def _to_index(url, index):
    parts = url.rsplit('/', 1)
    base_url, name = parts[0], parts[1]
    name = name.replace('.html', '')
    new_filename = f"{name}-10-{index}.html"
    new_url = f"{base_url}/{new_filename}"
    return new_url


def _get_total_indexes(soup: BeautifulSoup) -> int:
    tags = soup.css.select("div.changepage select#page option")
    # This HTML is duplacated in page
    # There one in top section, and another one below in below section
    return len(tags) // 2