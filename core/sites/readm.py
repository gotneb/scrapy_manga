from selenium import webdriver
from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.options import Options 
from selenium.common.exceptions import NoSuchElementException
from core.manga import Manga


def cli_driver() -> webdriver.Chrome:
    """Returns a webdriver which works without gui"""
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    return webdriver.Chrome(options=options)


def get_populars() -> list[Manga]:
    driver = cli_driver()
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


def manga_detail(manga_url) -> Manga:
    """Returns the manga data on the url."""
    driver = cli_driver()
    driver.get(manga_url)

    # Just for debug...
    #print(f"Openned {driver.title}")

    title = get_title(driver)
    alt_title = get_alt_title(driver)
    # I dunno if it's right... But in case there isn't an author, I'll fetch artist...
    # Why? See vagabond -> https://readm.org/manga/7872
    # There isn't  an author, because it was written by someone in the past, but Takehiro-sama has draw for us :)
    if len(get_author(driver)) == 0:
        author = get_artist(driver)
    else:
        author = get_author(driver)
    stt = get_status(driver)
    thumbnail = get_thumbnail(driver)
    genres = get_genres(driver)
    summary = get_summary(driver)
    chapters = get_chapters(driver)
    total_chapters = len(chapters)

    # Clean resources
    driver.quit()

    return Manga(title, alt_title, author, thumbnail, genres, summary, stt, chapters, total_chapters)


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
    # TODO: it's freaking' lazy that way. It must improve!
    # Add a more robust wait
    driver.implicitly_wait(1)
    buttons = driver.find_elements(By.CSS_SELECTOR, "section.episodes-box div#seasons-menu a")
    for e in buttons:
        e.click()
        allChapters = driver.find_elements(By.CSS_SELECTOR, "section.episodes-box div.ui.tab.active div.ui.list div.item.season_start h6.truncate a")
        for singleChapter in allChapters:
            # Usually ["Chapter", "__number__"]
            split = singleChapter.text.split()
            if (split.__len__() == 2):
                chapters.append(split[1])
    return chapters