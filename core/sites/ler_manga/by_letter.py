from typing import Callable
from bs4 import BeautifulSoup, Tag
from requests import get
from .constants import domain


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
    index = letter_min_index(letter)
    url = ""

    links = []
    while True:
        if index == 1:
            url = f"{domain}/mangas/?orderby=title&order=asc"
        else:
            url = f"{domain}/mangas/page/{index}/?orderby=title&order=asc"

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


# Helper functions to `get_all_start_with`
def _extract_link(tag: Tag) -> str:
    tags = tag.select("div.film-detail h3.film-name a")
    return tags[0].get("href")


# Helper function to `get_all_start_with`
def _link_start_with(link: str, letter: str) -> bool:
    name = link.split("/")[-2].lower()
    return name.startswith(letter)


# This is hardcode, so I literally saw those indexes on the site
# Just to improving the time. Since there's no way to achieve that by coding :(
def letter_min_index(letter: str) -> int:
    indexes = {
        "a": 2,
        "b": 8,
        "c": 13,
        "d": 17,
        "e": 23,
        "f": 25,
        "g": 28,
        "h": 31,
        "i": 37,
        "j": 46,
        "k": 48,
        "l": 56,
        "m": 60,
        "n": 69,
        "o": 72,
        "p": 76,
        "q": 79,
        "r": 79,
        "s": 83,
        "t": 94,
        "u": 108,
        "v": 110,
        "w": 111,
        "x": 113,
        "y": 115,
        "z": 118,
    }
    return indexes[letter]