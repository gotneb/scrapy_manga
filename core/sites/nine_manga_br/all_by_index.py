from typing import Callable

from bs4 import BeautifulSoup
from requests import get

MAX_INDEX = 501

def get_all_by_index(
    index: int, on_link_received: Callable[[str], None] = None
) -> list[str]:
    """
    Visits `br.ninemanga.com` and extract all links that are located in the specified `index`.

    Arguments:
    `index`: page's index.
    `on_link_received`: callback that's called when a link is received.
    """
    if index < 1:
        raise Exception('Index must be greather than 0!')
    if index > MAX_INDEX:
        msg = f'Index is must be less than {MAX_INDEX+1}!'
        raise Exception(msg)
    
    links = []
    url = f'https://br.ninemanga.com/category/index_{index}.html'
    soup = BeautifulSoup(get(url).content, "html.parser")
    tags = soup.css.select("div.leftbox ul.direlist li dl.bookinfo dt a")
    for a in tags:
        link = a.get('href')
        links.append(link)

        if on_link_received != None:
            on_link_received(link)

    return links