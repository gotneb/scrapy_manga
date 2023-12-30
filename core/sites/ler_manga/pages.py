import time
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from core.driver import init_driver


def get_pages(chapter_url: str) -> list[str]:
    """Extract all image links from a chapter.\n
    `chapter_url:` a chapter of a manga
    """
    soup = BeautifulSoup(_get_html(chapter_url), "html.parser")
    img_tags = soup.css.select("div.reader-area img")
    imgs = []
    for img in img_tags:
        imgs.append(img.get("src"))
    return imgs


# Helper function to get function `get_pages``
def _get_html(link) -> str:
    driver = init_driver(True, timeout=10)

    driver.get(link)
    options = driver.find_elements(By.CSS_SELECTOR, "div.nvs.slc select#slch option")
    options[-1].click()

    # Site might open a 2nd tab to show ads
    if len(driver.window_handles) == 2:
        # Close ADS tab
        driver.close()
        # Move to newly tab manga
        driver.switch_to.window(driver.window_handles[0])

    ARBITRARY_NUMBER_ATTEMPTS = 20
    ARBITRARY_SCROLL_AMOUNT = 700
    ARBITRARY_TIME = 0.05  # 50 ms

    for _ in range(0, ARBITRARY_NUMBER_ATTEMPTS):
        ActionChains(driver).scroll_by_amount(0, ARBITRARY_SCROLL_AMOUNT).perform()
        time.sleep(ARBITRARY_TIME)

    html = driver.page_source
    driver.close()
    return html