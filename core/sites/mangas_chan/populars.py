from typing import Callable
from selenium import webdriver
from bs4 import BeautifulSoup

from core.driver import *


def get_populars(on_link_received: Callable[[str], None] = None) -> list[str]:
    """Visits the `mangaschan.net` and returns top 100 most populars mangas right now."""
    links = []
    index = 1
    driver = init_driver(False)

    # Iterating 5 times returns 100 mangas
    for _ in range(0, 5):
        url = f'https://mangaschan.net/manga/?page={index}&status=&type=&order=popular'
        soup = BeautifulSoup(get_driver_html(driver, url), "html.parser")
        anchor_tags = soup.css.select("div.listupd div.bs a")
        
        for a in anchor_tags:
            link = a.get('href')
            links.append(link)

            if on_link_received != None:
                on_link_received(link)
        index += 1

    driver.quit()
    return links