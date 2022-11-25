from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options 


def get_highlights(driver):
    elems = driver.find_elements(By.CSS_SELECTOR, 'div.alinhamento.pdB-2 div.owl-stage-outer div.owl-item div.dados a')
    populars = []
    for tag in elems:
        title = tag.get_attribute('title')
        if title != '' and not populars.__contains__(title):
            populars.append(title) 
            print(title)
    return populars


def get_populars(driver):
    elems = driver.find_elements(By.CSS_SELECTOR, 'div.crw div.widget-content li.popular-treending.clear h4')
    releases = []
    for tag in elems:
        releases.append(tag.text)
        print(tag.text)
    return releases


def get_recent_releases(driver):
    elems = driver.find_elements(By.CSS_SELECTOR, 'div#recent_releases div#lancamento-hoje ul li.item_news-manga div.right h3 a')
    releases = []
    for tag in elems:
        releases.append(tag.text)
        print(tag.text)
    return releases


if __name__ == '__main__':
    options = Options()  
    options.add_argument("--headless") 
    driver = webdriver.Chrome(options=options)

    driver.get("https://mymangas.net/")

    print("\n[RECENT RELEASES]")
    get_recent_releases(driver)

    print("\n[HIGHLIGHTS]")
    get_highlights(driver)

    print("\n[POPULARS]")
    get_populars(driver)

    driver.quit()
