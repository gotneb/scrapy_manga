from typing import Callable

from bs4 import BeautifulSoup

from core.driver import *


def get_all_start_with(
    letter: str, show_window=False, on_link_received: Callable[[str], None] = None
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
    
    letter = letter.upper()
    links = []
    driver = init_driver(False)

    start = 1
    url = f'https://mangaschan.net/lista-de-a-z/page/{start}/?show={letter}'

    soup = BeautifulSoup(get_driver_html(driver, url), "html.parser")   
    anchor_tags = soup.css.select("div.page div.pagination a.page-numbers") 
    # Gets last but one number
    total = int(anchor_tags[len(anchor_tags) - 2].text)

    for index in range(start, total + 1):
        if index != 1:
            url = f'https://mangaschan.net/lista-de-a-z/page/{index}/?show={letter}'
            soup = BeautifulSoup(get_driver_html(driver, url), "html.parser")
        
        anchor_tags = soup.css.select("div.listo div.bsx a")
        for tag in anchor_tags:
            link = tag.get('href')
            links.append(link) 

            if on_link_received != None:
                on_link_received(link)

    driver.quit()
    return links