import time
import requests
import json
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
    elems = driver.find_elements(By.CSS_SELECTOR, 'div#recent_releases ul li.item_news-manga div.right h3 a')
    releases = []
    for tag in elems:
        link = tag.get_attribute("href")
        releases.append(link)
    return releases


def update_mangas():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=options)
    driver.get("https://readm.org/")

    #   print("\n[HIGHLIGHTS]")
    #   get_highlights(driver)

    #   print("\n[POPULARS]")
    #   get_populars(driver)

    print("\n[RECENT RELEASES]")
    releases = get_recent_releases(driver)

    print("Ready!")
    data = {
        "links": releases,
    }
    response = requests.post('https://mangahoot.up.railway.app/add/release-mangas/', json=data)

    if (response.status_code == 200):
        print("OK | response: ", response.content)
    else:
        print("Something went wrong... =(")
        print("response: ", response.content)

    driver.quit()


ONE_MINUTE = 60
while True:
    update_mangas()
    time.sleep(30 * ONE_MINUTE)