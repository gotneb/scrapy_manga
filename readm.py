from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options 


def get_manga():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=options)
    driver.get("https://readm.org/manga/berserk")
    # Get Title
    title = driver.find_element(By.CSS_SELECTOR, "div.ui.grid h1.page-title")
    print(title.text)
    # Get thumbnail
    thumbnail = driver.find_element(By.CSS_SELECTOR, "a#series-profile-image-wrapper img.series-profile-thumb")
    print(thumbnail.get_attribute("src"))
    # Get status
    status = driver.find_element(By.CSS_SELECTOR, "div.series-genres span.series-status.aqua")
    print(status.text)
    # Get tags
    genres = []
    elements = driver.find_elements(By.CSS_SELECTOR, "div.series-summary-wrapper div.ui.list div.item a")
    for e in elements:
        genres.append(e.text)
    print(genres)
    # Get Author
    author = driver.find_element(By.CSS_SELECTOR, "div.first_and_last span#first_episode small")
    print(author.text)
    # Get Artist
    artist = driver.find_element(By.CSS_SELECTOR, "div.first_and_last span#last_episode small")
    print(artist.text)
    # Get Summary
    elems = driver.find_elements(By.CSS_SELECTOR, "article.series-summary div.series-summary-wrapper p")
    summary = ""
    for e in elems:
        if (e.text != ""):
            summary += e.text
    print(summary)
    # Get chapters
    buttons = driver.find_elements(By.CSS_SELECTOR, "section.episodes-box div#seasons-menu a")
    for e in buttons:
        e.click()
        allChapters = driver.find_elements(By.CSS_SELECTOR, "section.episodes-box div.ui.tab.active div.ui.list div.item.season_start h6.truncate a")
        for singleChapter in allChapters:
            print(singleChapter.text.split()[1])
        #print(e.text)


if __name__ == "__main__":
    get_manga()