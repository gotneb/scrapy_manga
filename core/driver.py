from selenium import webdriver
import getpass
import os

_profile = 'selenium_manga'
_username = getpass.getuser()

def create_folder_if_not_exists(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)


def init_driver(show_window, timeout: int = 3) -> webdriver.Firefox:
    """
    Creates a webdriver.\n
    Arguments:  
        `show_window:` display firefox's window.
    Returns:
        A firefox's webdriver.
    """
    # Unix like only
    profile_path = f'/home/{_username}/.mozilla/firefox/{_profile}'
    create_folder_if_not_exists(profile_path)

    options = webdriver.FirefoxOptions()

    options.add_argument(f'-profile')
    options.add_argument(profile_path)

    if not show_window:
        options.add_argument('-headless')

    driver = webdriver.Firefox(options=options)
    driver.set_page_load_timeout(timeout)
    return driver


def get_driver_html(driver: webdriver.Firefox, url: str) -> str:
    """Returns the HTML content from a given driver."""
    try:
        driver.get(url)
    except:
        driver.execute_script("window.stop();")

    return driver.page_source