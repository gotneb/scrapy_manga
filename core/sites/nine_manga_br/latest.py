# External packages
from typing import Callable
from bs4 import BeautifulSoup, Tag
# Ours code
from requests import get

from .constants import *

# I'm not sure if I should have added a callback on this function o_o'
def get_latest_updates(
    limit: int = 0, on_link_received: Callable[[str], None] = None
) -> list[str]:
    """
    Returns a list of all links from `br.ninemanga.com` that were updateds.\n
    Arguments:
        `limit`: the total quantity of manga links will be extracted.
    """
    url = 'https://br.ninemanga.com/'
    links = []

    soup = BeautifulSoup(get(url).content, "html.parser")
    tags = soup.css.select("div.leftbox ul.homeupdate li a.show_book_desc")
    for a in tags:
        link = a.get('href')
        links.append(link)

        if on_link_received != None:
            on_link_received(link)

    return links