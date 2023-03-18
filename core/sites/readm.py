# Python
import math
from typing import Callable
# Selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait
# BS4
from bs4 import BeautifulSoup
# Requests
from requests import get
# Core
from core.driver import init_driver
from core.manga import Manga


domain = 'https://readm.org'


# I'm not sure if I should have added a callback on this function o_o'
def get_latest_updates(limit: int = 40, on_link_received: Callable[[str], None] = None) -> list[str]:
    """
    Returns a list of all links from `readm.org` that were updateds.\n
    Arguments:
        `limit:` the total quantity of manga links will be extracted.
    Return:
        A list of recent mangas updated.
    """
    # 400 it's equivalente to 10 page on "readm.org". The max is 10 pages!
    if limit > 400:
        raise Exception('limit must be lower or equals than 400!')

    links = []
    total_pages = math.ceil(limit/40)
    pages_counter = 0

    for page in range(1, total_pages + 1):
        html = get(f'https://readm.org/latest-releases/{page}')
        soup = BeautifulSoup(html.text, 'html.parser')

        all_h2 = soup.find_all('h2', class_='truncate')
        for h2 in all_h2:
            a = h2.find('a')
            # ERROR PRONE: adding two url's path may cause errors!
            link = domain + a['href']
            links.append(link)

            if on_link_received is not None:
                on_link_received(link)

            pages_counter += 1
            if pages_counter == limit:
                break
    
    return links


def get_pages(manga_url) -> list[str]:
    """Extract all image links from a manga chapter.

    `manga_url:` a chapter of a manga
    """
    if domain not in manga_url:
        raise Exception("get pages doesn't support this site!")

    html = get(manga_url)
    soup = BeautifulSoup(html.text, 'html.parser')
    url_imgs = []

    links = soup.find_all('img', class_='img-responsive')
    for link in links:
        href = link['src']
        url = f'{domain}{href}'
        url_imgs.append(url)

    return url_imgs


# TODO: Make it avaliable for "mangalivre.net" as well
def get_populars() -> list[Manga]:
    """Visits the `readm.org` and returns top 10 most populars mangas."""
    driver = init_driver()
    url = "https://readm.org/popular-manga"
    driver.get(url)

    # Links to mangas
    links = []
    elems = driver.find_elements(
        By.CSS_SELECTOR, "ul.filter-results li.mb-lg div.poster-with-subject a")
    for e in elems:
        anchor = e.get_attribute("href")
        if links.__len__() == 0:
            links.append(anchor)
        elif (not links.__contains__(anchor)) and (not anchor.__contains__("category")):
            links.append(anchor)

    mangas = []
    for link in links:
        mangas.append(manga_detail(link))
    return mangas


def get_all_start_with(letter, show_window=True, on_link_received: Callable[[str], None] = None) -> list[str]:
    """
    Visits `readm.org` and extract all links that starts with `letter` on its name.\n
    Arguments:
        `letter:` manga initial name.
        `show_window:` show google's chrome window.
        `on_link_received:` callback that's called when manga's link is received.
    Return:
        A list containing all links.
    """
    if len(letter) > 2:
        raise Exception('letter must be unique character.')

    letter = letter.lower()
    driver = init_driver(show_window)
    driver.get(f'https://readm.org/manga-list/{letter}')

    # Get all tags '<a>'
    all_links = []
    anchors = driver.find_elements(
        By.CSS_SELECTOR, 'li div.poster.poster-xs a')
    for a in anchors:
        link = a.get_attribute('href')
        all_links.append(link)
        # Callback
        if on_link_received is not None:
            on_link_received(link)

    return all_links


# FIX: Disabling chrome's window may throw errors
def manga_detail(manga_url, show_window=True) -> Manga:
    """
    Visits the `manga_url` and extract all data on it.
    Arguments:
        manga_url: the manga content. Must have `readm.org` or `mangalivre.net` domain.
        enable_gui: show chrome window.
    Return:
        Manga content.
    """
    driver = init_driver(show_window)
    driver.get(manga_url)

    # Just for debug...
    # print(f"Openned {driver.title}")

    title = get_title(driver)
    alt_title = get_alt_title(driver)
    author = get_author(driver)
    artist = get_artist(driver)
    stt = get_status(driver)
    thumbnail = get_thumbnail(driver)
    genres = get_genres(driver)
    summary = get_summary(driver)
    chapters = get_chapters(driver)
    total_chapters = len(chapters)

    # Clean resources
    driver.quit()

    return Manga(title, alt_title, author, artist, thumbnail, genres, summary, stt, total_chapters, chapters)


def get_title(driver) -> str:
    """Returns title from manga"""
    title = driver.find_element(By.CSS_SELECTOR, "div.ui.grid h1.page-title")
    return title.text


def get_alt_title(driver) -> str:
    """Returns alternative title from manga"""
    try:
        title = driver.find_element(By.CSS_SELECTOR, "div.sub-title.pt-sm")
        return title.text
    except NoSuchElementException:
        return ''


def get_author(driver) -> str:
    """Returns author from manga. If does not exist, hence it returns an empty str."""
    try:
        elem = driver.find_element(
            By.CSS_SELECTOR, "div.first_and_last span#first_episode small")
        return elem.text
    except NoSuchElementException:
        return ""


def get_artist(driver) -> str:
    """Returns author from manga. If does not exist, hence it returns an empty str."""
    try:
        e = driver.find_element(
            By.CSS_SELECTOR, "div.first_and_last span#last_episode small")
        return e.text
    except NoSuchElementException:
        return ""


def get_thumbnail(driver) -> str:
    """Returns thumbnail (image) from manga."""
    elem = driver.find_element(
        By.CSS_SELECTOR, "a#series-profile-image-wrapper img.series-profile-thumb")
    return elem.get_attribute("src")


def get_status(driver) -> str:
    """Returns status from manga. If does not exist, hence it returns an empty str."""
    try:
        elem = driver.find_element(
            By.CSS_SELECTOR, "div.series-genres span.series-status.aqua")
        return elem.text
    except NoSuchElementException:
        return ""


def get_genres(driver) -> list[str]:
    """Returns a list of genres from manga."""
    genres = []
    elements = driver.find_elements(
        By.CSS_SELECTOR, "div.series-summary-wrapper div.ui.list div.item a")
    for e in elements:
        genres.append(e.text)
    return genres


def get_summary(driver) -> str:
    """Returns summary from manga."""
    elems = driver.find_elements(
        By.CSS_SELECTOR, "article.series-summary div.series-summary-wrapper p")
    summary = ""
    for e in elems:
        if (e.text != ""):
            summary += e.text
    return summary


def get_chapters(driver) -> list[str]:
    """Returns a list of chapters from manga."""
    chapters = []
    MAX_TIME = 60  # 1 minute

    buttons = WebDriverWait(driver, MAX_TIME).until(lambda d: d.find_elements(
        By.CSS_SELECTOR, "section.episodes-box div#seasons-menu a"))

    # Some `ADS` interrupts driver avoiding it to click on button
    # To fix I'm explicitly scrolling the window to bottom
    driver.execute_script("window.scrollBy(0, 1000);")

    for e in buttons:
        e.click()
        allChapters = driver.find_elements(
            By.CSS_SELECTOR, "section.episodes-box div.ui.tab.active div.ui.list div.item.season_start h6.truncate a")
        for singleChapter in allChapters:
            # Usually ["Chapter", "__number__"]
            split = singleChapter.text.split()
            if (len(split) == 2):
                chapters.append(split[1])
    return chapters
