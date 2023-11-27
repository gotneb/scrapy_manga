# External packages
import time
from bs4 import BeautifulSoup
from core.driver import get_driver_html, init_driver
# Our code
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver

ARBITRARY_NUMBER_ATTEMPTS = 20
ARBITRARY_SCROLL_AMOUNT = 500
ARBITRARY_TIME = 0.1 # 100 ms
LOADING_SVG = 'https://mangaschan.net/wp-content/themes/mangareader/assets/img/readerarea.svg'

def _scroll_page(driver: webdriver.Firefox):
    for _ in range(0, ARBITRARY_NUMBER_ATTEMPTS):
        ActionChains(driver)      \
        .scroll_by_amount(0, ARBITRARY_SCROLL_AMOUNT) \
        .perform()
        time.sleep(ARBITRARY_TIME)


def _get_total_pages(driver: webdriver.Firefox):
    elems = driver.find_elements(By.CSS_SELECTOR, 'span.navlef select#select-paged.ts-select-paged option')
    return len(elems)


def get_pages(chapter_url: str) -> list[str]:
    """Extract all image links from a chapter.\n
    `chapter_url:` a chapter of a manga
    """
    driver = init_driver(False, timeout=10)
    driver.get(chapter_url)
    total = _get_total_pages(driver)
    imgs = []

    while len(imgs) != total:
        elems = driver.find_elements(By.CSS_SELECTOR, 'div#readerarea img')
        for tag in elems:
            link = tag.get_attribute('src')
            if link != LOADING_SVG and link not in imgs:
                imgs.append(link)

                print(link)
        _scroll_page(driver)

    driver.quit()
    return imgs