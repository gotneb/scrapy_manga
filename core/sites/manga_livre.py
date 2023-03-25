# Core
import time
from core.driver import init_driver
# Selenium
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By

from core.manga import Manga


def manga_detail(manga_url, show_window=True):
    """
    Visits the `manga_url` and extract all data on it.\n
    Arguments:
        manga_url: the manga content. Must be `mangalivre.net` domain.
        enable_gui: show chrome window.
    Return:
        Manga content.
    """
    driver = init_driver(show_window)
    driver.get(manga_url)

    # Just for debug...
    # print(f"Openned {driver.title}")

    title = get_title(driver)
    genres = get_genres(driver)
    author = get_author(driver)
    summary = get_summary(driver)
    thumbnail = get_thumbnail(driver)
    # TODO: Get chapters
    chapters = ['']
    #chapters = get_chapters(driver)

    # Clean resources
    driver.quit()

    return Manga(title, 'alt_title', author, 'artist', thumbnail, genres, summary, 'stt', 'total_chapters', chapters)


def get_thumbnail(driver: webdriver.Chrome):
    elem = driver.find_element(By.CSS_SELECTOR, 'div.series-img div.cover img')
    img = elem.get_attribute('src')
    return img


def get_summary(driver: webdriver.Chrome):
    elem = driver.find_element(By.CSS_SELECTOR, 'div#series-desc span.series-desc span')
    desc = elem.text
    return desc


def get_author(driver: webdriver.Chrome):
    span_tag = driver.find_element(By.CSS_SELECTOR, 'div#series-data.content-wraper div.series-info.touchcarousel span.series-author')
    a_tag = span_tag.find_element(By.TAG_NAME, 'a')
    
    span_text = span_tag.text
    a_text = a_tag.text

    author = span_text.replace(a_text, '').strip()
    return author


def get_title(driver: webdriver.Chrome) -> str:
    elem = driver.find_element(By.CSS_SELECTOR, 'div#series-data.content-wraper div.series-info.touchcarousel span.series-title')
    title = elem.text
    return title


def get_summary(driver: webdriver.Chrome) -> str:
    elem = driver.find_element(By.CSS_SELECTOR, 'div#series-desc span.series-desc span')
    desc = elem.text
    return desc


def get_genres(driver: webdriver.Chrome) -> list[str]:
    # kkkk I don't even know if it's allowed type that way :D
    elems = driver.find_elements(
    By.CSS_SELECTOR,
    'div#series-data.content-wraper div.series-info.touchcarousel div.touchcarousel-wrapper ul.tags.touchcarousel-container li')

    genres = []
    for li in elems:
        genres.append(li.text)


def get_chapters(driver: webdriver.Chrome):
    # TODO: scroll the entire content
    while True:
        ActionChains(driver)       \
        .scroll_by_amount(0, 1000) \
        .perform()
        #time.sleep(1/10)

        first = driver.find_element(By.CSS_SELECTOR, 'div.loadmore a.loadmore')
        second = driver.find_element(By.CSS_SELECTOR, 'div.loadmore a.loading.loadmore')

        st1 = first.get_attribute('style')
        st2 = second.get_attribute('style')

        if st1 == 'display: none;' and st1 == st2:
            print(f'1 | {st1}\n2 | {st2}')

    elems = driver.find_elements(By.CSS_SELECTOR, 'div.container-box.default.color-brown ul.full-chapters-list.list-of-chapters li a.link-dark')
    for a in elems:
        # title's attribute returns: 'Ler Capitulo `N`', where N is a number =P
        title = a.get_attribute('title').split(' ')[2] 
        print(title)
