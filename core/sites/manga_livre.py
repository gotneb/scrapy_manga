# Python
import math
from typing import Callable

# Selenium
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By

# BeautifulSoup4
from bs4 import BeautifulSoup

# Core
from core.driver import init_driver

# Entities
from entities.chapter_info import ChapterInfo
from entities.manga import Manga

_origin = "manga_livre"
_language = "portuguese"


def get_populars(on_link_received: Callable[[str], None] = None) -> list[str]:
    """Visits the `mangalivre.net` and returns top 10 most populars in the day mangas."""
    url = 'https://mangalivre.net/lista-de-mangas/ordenar-por-numero-de-leituras/todos/dia'
    links = []
    counter = 0

    driver = init_driver(show_window=False)
    driver.get(url)

    elems = driver.find_elements(By.CSS_SELECTOR, 'div.content-wraper ul.seriesList li a[href]')
    for tag in elems:
        if counter == 10:
            break

        link = tag.get_attribute('href')
        links.append(link)

        # Callback
        if on_link_received is not None:
            on_link_received(link)

        counter += 1
    
    return links


def get_latest_updates(
    limit: int = 30, on_link_received: Callable[[str], None] = None
) -> list[str]:
    """
    Returns a list of all links from `mangalivre.net` that were updated.\n
    Arguments:
    `limit:` the total quantity of manga links will be extracted.\n
    Return:
    A list of recent mangas links that were updated.
    """
    # Mangá Livre gives 30 mangas by page...
    counter = 0
    total_pages = math.ceil(limit / 30)
    path = "https://mangalivre.net/lista-de-mangas/ordenar-por-atualizacoes"

    # Setup
    mangas_urls = []
    driver = init_driver(show_window=False)
    for index in range(1, total_pages + 1):
        if counter == limit:
            break

        driver.get(f"{path}?page={index}")
        # Get a list of all mangas links
        anchor_tags = driver.find_elements(
            By.CSS_SELECTOR, "div.content-wraper ul.seriesList li a[href]"
        )
        for a in anchor_tags:
            link = a.get_attribute("href")
            mangas_urls.append(link)

            # Callback
            if on_link_received is not None:
                on_link_received(link)

            counter += 1
            if counter == limit:
                break

    driver.close()
    return mangas_urls


def get_pages(manga_url: str) -> list[str]:
    """Extract all image links from a manga chapter.\n
    `manga_url:` manga chapter
    """
    driver = init_driver(show_window=False)
    driver.get(manga_url)

    # Toggle to vertical mode
    try:
        btn = driver.find_element(
            By.CSS_SELECTOR,
            "div.orientation-container.orientation-toggle a.orientation span.change-to-vertical",
        )
        btn.click()
    except:
        print("ALREADY IN VERTICAL MODE!")

    # For adult content, agree I'm older than 18 years
    try:
        btn = driver.find_element(
            By.CSS_SELECTOR, "div.adult-warning-wrapper a.eighteen-but"
        )
        btn.click()
    except:
        print("NOT AN ADULT CONTENT")

    while True:
        elem = driver.find_element(By.CSS_SELECTOR, "div.loading")

        # When all pages were loaded, the 'style' is triggered
        # Before that, it doesn't have any value
        if len(elem.get_attribute("style")) > 1:
            break

        ActionChains(driver).scroll_by_amount(0, 200).perform()

    pages = []
    elems = driver.find_elements(By.CSS_SELECTOR, "div.manga-image picture img")
    for img in elems:
        src = img.get_attribute("src")
        pages.append(src)

    return pages


def manga_detail(url: str, show_window=False):
    """
    Visits the `manga_url` and extract all data on it.

    Arguments:

    `manga_url:` the url of manga site.

    `enable_gui:` optional, show chrome window.
    """
    driver = init_driver(show_window)
    driver.get(url)

    # "Manga Livre" mangas doesn't have an artist data at all
    artist = None
    # "Manga Livre" mixes author and status on the same tag ¯\_(ツ)_/¯
    author, status = get_author(driver)

    title = get_title(driver)
    score = get_score(driver)
    alt_title = get_alt_title(driver)
    summary = get_summary(driver)
    thumbnail = get_thumbnail(driver)
    chapters_info = get_chapters_info(driver)
    genres = get_genres(driver)

    # Clean resources
    driver.quit()

    return Manga(
        title=title,
        alternative_title=alt_title,
        author=author,
        artist=artist,
        status=status,
        url=url,
        origin=_origin,
        language=_language,
        thumbnail=thumbnail,
        genres=genres,
        summary=summary,
        chapters_info=chapters_info,
        rating=score,
    )


# Helper function to `get_all_start_with`
def _check_page_exists(driver: webdriver.Chrome) -> bool:
    try:
        h1_tag = driver.find_element(By.CSS_SELECTOR, "div.content-wrapper h1")
        err = h1_tag.text
        if err == "ERRO DE SERVIDOR":
            return False
        else:
            # I'm almost sure the program won't never reach here...
            return True
    except:
        return True


def get_all_start_with(
    letter: str, show_window=False, on_link_received: Callable[[str], None] = None
) -> list[str]:
    if len(letter) > 2:
        raise Exception("letter must be an unique character.")

    # Setup
    letter = letter.lower()
    path = "https://mangalivre.net/lista-de-mangas/ordenar-por-nome"
    url = f"{path}/{letter}"
    driver = init_driver(show_window=show_window)
    driver.get(url)

    # Mangá Livre has many mangas, but they are spllited in in a group of 30
    # We don't know in advance haw many times they splitted.
    # So we just keep going until the end
    mangas_links = []
    index = 1
    while True:
        if not _check_page_exists(driver):
            print(f"Page on index {index} there isn't.")
            break

        # Get a list of all mangas
        anchor_tags = driver.find_elements(
            By.CSS_SELECTOR, "div.content-wraper ul.seriesList li a[href]"
        )
        for a in anchor_tags:
            link = a.get_attribute("href")
            mangas_links.append(link)

            # Callback
            if on_link_received is not None:
                on_link_received(link)

        # Update
        index += 1
        url = f"{path}/{letter}?page={index}"
        driver.get(url)

    driver.close()
    return mangas_links


def get_score(driver: webdriver.Chrome) -> float:
    elem = driver.find_element(
        By.CSS_SELECTOR, "div.series-img div.score div.score-number"
    )
    score = elem.text
    return float(score)


def get_thumbnail(driver: webdriver.Chrome):
    elem = driver.find_element(By.CSS_SELECTOR, "div.series-img div.cover img")
    img = elem.get_attribute("src")
    return img


def get_summary(driver: webdriver.Chrome):
    elem = driver.find_element(By.CSS_SELECTOR, "div#series-desc span.series-desc span")
    desc = elem.text
    return desc


def get_author(driver: webdriver.Chrome):
    span_tag = driver.find_element(
        By.CSS_SELECTOR,
        "div#series-data.content-wraper div.series-info.touchcarousel span.series-author",
    )
    span_text = span_tag.text

    # For some unkown reason, the manga page sometimes has a
    # specific tag containing the author, and sometimes it doesn't happen
    try:
        a_tag = span_tag.find_element(By.TAG_NAME, "a")
        a_text = a_tag.text
        author = span_text.replace(a_text, "").strip()
    except:
        author = span_text

    # TODO: Make the below code as function for extract status =P
    status = "COMPLETO"
    if status in author:
        author = author.replace(status, "").strip()
    else:
        status = "EM ANDAMENTO"

    return author, status


def get_title(driver: webdriver.Chrome):
    elem = driver.find_element(
        By.CSS_SELECTOR,
        "div#series-data.content-wraper div.series-info.touchcarousel span.series-title",
    )
    title = elem.text
    return title


def get_summary(driver: webdriver.Chrome) -> str:
    elem = driver.find_element(By.CSS_SELECTOR, "div#series-desc span.series-desc span")
    desc = elem.text
    return desc


def get_genres(driver: webdriver.Chrome) -> list[str]:
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")

    genres = []
    elems = soup.find_all("li", class_="touchcarousel-item")
    for li in elems:
        a_tag = li.find("a")
        # DEBUG: Find out why `a_tag` sometimes is `None`
        # It's crucial to know in advance why is this happening
        if a_tag is not None:
            span_tag = a_tag.find("span", class_="button")
            genres.append(span_tag.text)
    return genres


def get_alt_title(driver: webdriver.Chrome) -> str:
    elems = driver.find_elements(
        By.CSS_SELECTOR, "div#series-desc span.series-desc ol.series-synom li"
    )

    li_texts = []
    for li in elems:
        li_texts.append(li.text)
    
    alt_title = ', '.join(li_texts)
    print(alt_title)

    return alt_title


def get_chapters_info(driver: webdriver.Chrome) -> list[ChapterInfo]:
    # PROBLEM:
    # Chapters are loaded lazily by AJAX.
    # There isn't a specific time where I can know in advance when the page has fully loaded.
    #
    # HOW IT WORKS:
    # There's a specific div notifying user when content is being loaded
    # Every time we scroll this div, it updates its children "style"
    # When it's done, all chidren have block style "none", I think it loads about 250 chapters...
    # So I've putted a "limiter". I think 50 it's a great amount.
    #
    # DON'T WORRY:
    # Once all chapters were loaded, the div children will have the same display
    # Meaning the counter will quickly increment to "limit".

    limit = 50
    counter = 0
    while counter < limit:
        # Scroll the page indefinitely
        ActionChains(driver).scroll_by_amount(0, 1000).perform()

        # Site notifies users that chapters are being loaded
        first = driver.find_element(By.CSS_SELECTOR, "div.loadmore a.loadmore")
        second = driver.find_element(By.CSS_SELECTOR, "div.loadmore a.loading.loadmore")
        st1 = first.get_attribute("style")
        st2 = second.get_attribute("style")

        if st1 == "display: none;" and st1 == st2:
            counter += 1

    # When fully loaded, we can extract data
    elems = driver.find_elements(
        By.CSS_SELECTOR,
        "div.container-box.default.color-brown ul.full-chapters-list.list-of-chapters li a.link-dark",
    )
    chapters = []
    for a in elems:
        # title's attribute returns: 'Ler Capitulo `N`', where N is a number =P
        value = a.get_attribute("title").split(" ")[2]
        id = _get_chapter_id(a.get_attribute("href"))
        chapters.append(ChapterInfo(name=value, id=id))

    return chapters


def _get_chapter_id(a_tag: str) -> str:
    """Get an internal id from a chapter.
    Arguments:\n
    `a_tag`: the chapter link to read
    """
    splitted = a_tag.split("/")
    # Python indexes are weird as hell
    # Last but one
    return splitted[-2]
