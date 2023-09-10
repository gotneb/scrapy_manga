import os
from selenium.webdriver.common.by import By
from selenium.webdriver import Chrome
from selenium.webdriver.remote.webelement import WebElement 
from core.driver import init_driver
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep

def try_to_login(driver: Chrome):
    """Verifies if user is logged. Otherwise logins."""
    buttons = driver.find_elements(By.CSS_SELECTOR, 'div#user div.left.floated.author a.ui.button.secondary')
    for btn in buttons:
        # This button only displays when the user hasn't entered yet
        if "sign in" == btn.text.lower():
            # input('Pess any key to continue...')
            make_login(driver, btn)


# Assumes you are not logged
def make_login(driver: Chrome, loginButton: WebElement):
    # Header button to show login box
    loginButton.click()
    # Email field
    email = driver.find_element(By.CSS_SELECTOR, 'div.swal2-content input#lb-email')
    email.send_keys(os.getenv('READM_EMAIL'))
    # Password field
    password = driver.find_element(By.CSS_SELECTOR, 'div.swal2-content input#lb-password')
    password.send_keys(os.getenv('READM_PASSWORD'))
    # Needed 'cause chapters might not being displayed until a amount of time has elipsed
    driver.implicitly_wait(1.0)
    # Submit button to actually login
    driver.find_element(
        By.CSS_SELECTOR, 'button.swal2-confirm.swal2-styled'
    )\
    .click()


def extract_manga_page(manga_url) -> str:
    """
    Visits `manga_url` using Selenium and extracts data.

    If not logged in, logs into.
    """
    if os.getenv('READM_EMAIL') == None     \
    or os.getenv('READM_PASSWORD') == None  \
    or len(os.getenv('READM_EMAIL')) == 0   \
    or len(os.getenv('READM_PASSWORD')) == 0:
        raise Exception("Readm email/password wasn't defined on .env!")

    driver = init_driver(False)
    # Loads page even more faster
    driver.set_page_load_timeout(10)

    try:
        driver.get(manga_url)
    except:
        driver.execute_script("window.stop();")

    
    try_to_login(driver)
    
    ActionChains(driver).scroll_by_amount(0, 1000).perform()
    sleep(2)

    html = driver.page_source
    driver.quit()

    return html