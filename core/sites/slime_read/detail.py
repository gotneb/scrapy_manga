# External packages
from core.driver import init_driver
# Ours code
from entities.chapter_info import ChapterInfo
from entities.manga import Manga
from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By

from .constants import origin
from .constants import language

def manga_detail(manga_url, show_window=False):
    """
    Visits the `manga_url` and extract all data on it.\n
    Arguments:\n
    `manga_url:` the manga content.
    `enable_gui:` show chrome window.
    """
    driver = init_driver(True, timeout=10)
    driver.get(manga_url)

    title = _get_title(driver)
    alt_title = None
    status = _get_status(driver)
    author, artist = None, None
    score = None
    thumbnail = _get_thumbnail(driver)
    genres = _get_genres(driver)
    summary = _get_summary(driver)
    chapters_info = _get_chapters(driver)

    driver.quit()

    return Manga(
        title=title,
        alternative_title=alt_title,
        author=author,
        artist=artist,
        status=status,
        url=manga_url,
        origin=origin,
        language=language,
        thumbnail=thumbnail,
        genres=genres,
        summary=summary,
        chapters_info=chapters_info,
        rating=score,
    )


def _get_title(driver: Firefox) -> str:
    """Returns manga's title."""
    elem = driver.find_element(By.CSS_SELECTOR, 'div.mt-4 p')
    title = elem.text
    return title


def _get_status(driver: Firefox) -> str:
    """Returns manga's status."""
    elems = driver.find_elements(By.CSS_SELECTOR, 'div.mt-4 p')
    status = elems[-1].text
    status = status.split(':')[-1].strip()
    return status


def _get_thumbnail(driver: Firefox) -> str:
    """Returns manga's thumbnail."""
    elem = driver.find_element(By.CSS_SELECTOR, 'img.flex.rounded')
    thumb = elem.get_attribute('src')
    return thumb


def _get_summary(driver: Firefox) -> str:
    """Returns manga's summary."""
    elem = driver.find_element(By.CSS_SELECTOR, "div.mt-2.undefined p")
    summary = elem.text.strip()
    return summary


def _get_genres(driver: Firefox) -> list[str]:
    """Returns manga's genres."""
    genres = []
    elems = driver.find_elements(By.CSS_SELECTOR, 'div.mt-2.undefined a p')

    for tag in elems:
        genre = tag.text.strip()
        genres.append(genre)

    return genres


def _get_chapters(driver: Firefox) -> list[ChapterInfo]:
    """Returns manga's chapters."""
    chapters = []
    elems = driver.find_elements(By.CSS_SELECTOR, 'section.mt-2 div.mt-2 a p')
    for tag in elems:
        text = tag.text.strip().lower()
        if 'cap' in text:
            chapter = text.split(' ')[1]
            chapters.append(chapter)

    print(chapters)
    return chapters