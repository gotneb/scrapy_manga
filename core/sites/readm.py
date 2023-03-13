from typing import Callable, NoReturn

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait
from core.manga import Manga


def get_driver(show_window) -> webdriver.Chrome:
    """
    Creates a webdriver. If `show_window` is true, then display chrome window.\n
    Arguments:  
        show_window: shows google chrome's window.
    Returns:
        A google's webdriver.
    """
    # TODO: Throw exception if chrome is not installed
    options = webdriver.ChromeOptions()
    if not show_window:
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
    return webdriver.Chrome(options=options)

# TODO: Make it avaliable for "mangalivre.net" as well
def get_populars() -> list[Manga]:
    """Visits the `readm.org` and returns top 10 most populars mangas."""
    driver = get_driver()
    url = "https://readm.org/popular-manga"
    driver.get(url)

    # Links to mangas
    links = []
    elems = driver.find_elements(By.CSS_SELECTOR, "ul.filter-results li.mb-lg div.poster-with-subject a")
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


def get_all_start_with(letter, show_window=True, on_link_received: Callable[[str], NoReturn]=None) -> list[str]:
    """
    Visits `readm.org` and extract all links that starts with `letter` on its name.\n
    Arguments:
        letter: manga initial name.
        show_window: show google's chrome window.
        on_link_received: callback that's called when manga's link is received.
    Return:
        A list containing all links.
    """
    if len(letter) > 2:
        raise Exception('letter must be unique character.')

    letter = letter.lower()
    driver = get_driver(show_window)
    driver.get(f'https://readm.org/manga-list/{letter}')

    # Get all tags '<a>'
    all_links = []
    anchors = driver.find_elements(By.CSS_SELECTOR, 'li div.poster.poster-xs a')
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
    driver = get_driver(show_window)
    driver.get(manga_url)

    # Just for debug...
    #print(f"Openned {driver.title}")

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
        elem = driver.find_element(By.CSS_SELECTOR, "div.first_and_last span#first_episode small")
        return elem.text
    except NoSuchElementException:
        return ""


def get_artist(driver) -> str:
    """Returns author from manga. If does not exist, hence it returns an empty str."""
    try:
        e = driver.find_element(By.CSS_SELECTOR, "div.first_and_last span#last_episode small")
        return e.text
    except NoSuchElementException:
        return ""


def get_thumbnail(driver) -> str:
    """Returns thumbnail (image) from manga."""
    elem = driver.find_element(By.CSS_SELECTOR, "a#series-profile-image-wrapper img.series-profile-thumb")
    return elem.get_attribute("src")


def get_status(driver) -> str:
    """Returns status from manga. If does not exist, hence it returns an empty str."""
    try:
        elem = driver.find_element(By.CSS_SELECTOR, "div.series-genres span.series-status.aqua")
        return elem.text
    except NoSuchElementException:
        return ""


def get_genres(driver) -> list[str]:
    """Returns a list of genres from manga."""
    genres = []
    elements = driver.find_elements(By.CSS_SELECTOR, "div.series-summary-wrapper div.ui.list div.item a")
    for e in elements:
        genres.append(e.text)
    return genres


def get_summary(driver) -> str:
    """Returns summary from manga."""
    elems = driver.find_elements(By.CSS_SELECTOR, "article.series-summary div.series-summary-wrapper p")
    summary = ""
    for e in elems:
        if (e.text != ""):
            summary += e.text
    return summary


def get_chapters(driver) -> list[str]:
    """Returns a list of chapters from manga."""
    chapters = []
    MAX_TIME = 60 # 1 minute

    buttons = WebDriverWait(driver, MAX_TIME).until(lambda d: d.find_elements(By.CSS_SELECTOR, "section.episodes-box div#seasons-menu a"))

    # Some `ADS` interrupts driver avoiding it to click on button
    # To fix I'm explicitly scrolling the window to bottom
    driver.execute_script("window.scrollBy(0, 1000);")

    for e in buttons:
        e.click()
        allChapters = driver.find_elements(By.CSS_SELECTOR, "section.episodes-box div.ui.tab.active div.ui.list div.item.season_start h6.truncate a")
        for singleChapter in allChapters:
            # Usually ["Chapter", "__number__"]
            split = singleChapter.text.split()
            if (split.__len__() == 2):
                chapters.append(split[1])
    return chapters