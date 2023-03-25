# Core
from core.driver import init_driver
# Selenium
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By

from core.manga import Manga


def manga_detail(manga_url: str, show_window=True):
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

    # "Manga Livre" mangas doesn't have an artist data at all
    artist = None
    # "Manga Livre" mixes author and status on the same tag ¯\_(ツ)_/¯
    author, status = get_author(driver)

    title = get_title(driver)
    alt_title = get_alt_title(driver)
    genres = get_genres(driver)
    summary = get_summary(driver)
    thumbnail = get_thumbnail(driver)
    chapters = get_chapters(driver)
    total_chapters = len(chapters)

    # Clean resources
    driver.quit()

    return Manga(title=title, 
                 alternative_title=alt_title, 
                 author=author, 
                 artist=artist, 
                 thumbnail=thumbnail, 
                 genres=genres, 
                 summary=summary, 
                 status=status, 
                 total_chapters=total_chapters, 
                 chapters=chapters)


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
    span_text = span_tag.text

    # For some unkown reason, the manga page sometimes has a
    # specific tag containing the author, and sometimes it doesn't happen
    try:
        a_tag = span_tag.find_element(By.TAG_NAME, 'a')
        a_text = a_tag.text
        author = span_text.replace(a_text, '').strip()
    except:
        author = span_text

    # TODO: Make the below code as function for extract status =P
    status = "COMPLETO"
    if status in author:
        author = author.replace(status, '').strip()
    else:
        status = "EM ANDAMENTO"

    return author, status


def get_title(driver: webdriver.Chrome):
    elem = driver.find_element(By.CSS_SELECTOR, 'div#series-data.content-wraper div.series-info.touchcarousel span.series-title')
    title = elem.text
    return title


def get_summary(driver: webdriver.Chrome) -> str:
    elem = driver.find_element(By.CSS_SELECTOR, 'div#series-desc span.series-desc span')
    desc = elem.text
    return desc


def get_genres(driver: webdriver.Chrome) -> list[str]:
    # Is that way wrong? I mean... I don't think this kinda syntax looks like weird :P
    elems = driver.find_elements(
    By.CSS_SELECTOR,
    'div#series-data.content-wraper div.series-info.touchcarousel div.touchcarousel-wrapper ul.tags.touchcarousel-container li')

    genres = []
    for li in elems:
        genres.append(li.text)
    
    return genres


def get_alt_title(driver: webdriver.Chrome) -> str:
    elems = driver.find_elements(By.CSS_SELECTOR, 'div#series-desc span.series-desc ol.series-synom li')

    alt_title = ''
    for li in elems:
        if is_oriental(li.text):
            alt_title = li.text
            break
    
    return alt_title


def get_chapters(driver: webdriver.Chrome):
    # PROBLEM:
    # Chapters are loaded lazily by AJAX.
    # There isn't a specific time where I can know in advance when the page has fully loaded.
    # 
    # HOW IT WORKS:
    # There's a specific div notifying user when content is being loaded
    # Every time we scroll this div, it updates its children "style"
    # When it's done, all chidren have block style "none", it loads about 250 chapters...
    # So I've putted a "limiter". I think 50 it's a great amount.
    #
    # DON'T WORRY: 
    # Once all chapters were loaded, the div children will have the same display
    # Meaning the counter will quickly increment to "limit".

    limit = 50
    counter = 0
    while counter < limit:
        # Scroll the page indefinitely
        ActionChains(driver)       \
        .scroll_by_amount(0, 1000) \
        .perform()

        # Site notifies users that chapters are being loaded
        first = driver.find_element(By.CSS_SELECTOR, 'div.loadmore a.loadmore')
        second = driver.find_element(By.CSS_SELECTOR, 'div.loadmore a.loading.loadmore')
        st1 = first.get_attribute('style')
        st2 = second.get_attribute('style')

        if st1 == 'display: none;' and st1 == st2:
            counter += 1

    # When fyllu loaded, we can extract data
    elems = driver.find_elements(By.CSS_SELECTOR, 'div.container-box.default.color-brown ul.full-chapters-list.list-of-chapters li a.link-dark')
    chapters = []
    for a in elems:
        # title's attribute returns: 'Ler Capitulo `N`', where N is a number =P
        chapter_value = a.get_attribute('title').split(' ')[2] 
        chapters.append(chapter_value)
    
    return chapters


def is_oriental(word: str) -> bool:
    return not word.isascii() 
