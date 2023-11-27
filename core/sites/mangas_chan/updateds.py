import math
from core.driver import *
from typing import Callable
from bs4 import BeautifulSoup

MANGAS_PER_PAGE = 30
TOTAL = MANGAS_PER_PAGE * 10

# I'm not sure if I should have added a callback on this function o_o'
def get_latest_updates(
    limit: int = 30, on_link_received: Callable[[str], None] = None
) -> list[str]:
    """
    Returns a list of all links from `mangaschan.net` that were updateds.\n
    Arguments:
        `limit:` the total quantity of manga links will be extracted.
    Return:
        A list of recent mangas updated.
    """
    if limit > TOTAL:
        raise Exception(f"limit must be lower or equals than {TOTAL}!")

    links = []
    total_pages = math.ceil(limit / MANGAS_PER_PAGE)
    pages_counter = 0

    driver = init_driver(False)

    for page in range(1, total_pages + 1):
        url = f"https://mangaschan.net/ultimas-atualizacoes/page/{page}/"
        soup = BeautifulSoup(get_driver_html(driver, url), "html.parser")

        anchor_tags = soup.css.select("div.uta div.luf a.series") 
        for tag in anchor_tags:
            link = tag.get('href')
            links.append(link)

            if on_link_received is not None:
                on_link_received(link)

            pages_counter += 1
            if pages_counter == limit:
                break

    return links