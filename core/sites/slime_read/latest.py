# External packages
from typing import Callable
from core.driver import init_driver
# Ours code
from entities.chapter_info import ChapterInfo
from entities.manga import Manga
from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By

def get_updates(
    on_link_received: Callable[[str], None] = None
) -> list[str]:
    """
    Returns a list of all links from site that were recently updateds.

    Arguments:
    `on_link_received`: callback when a new link is found.
    """
    links = []

    driver = init_driver(True, timeout=30)
    driver.get('https://slimeread.com')

    elems = driver.find_elements(By.CSS_SELECTOR, 'section.mt-2 div.bg-card > a')
    for tag in elems:
        link = tag.get_attribute('href')
        links.append(link)

        if on_link_received != None:
            on_link_received(link)

    driver.quit()

    return links