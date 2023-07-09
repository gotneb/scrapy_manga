from selenium import webdriver
import getpass

_profile = 'selenium_manga'
_username = getpass.getuser()

def init_driver(show_window) -> webdriver.Chrome:
    """
    Creates a webdriver.\n
    Arguments:  
        `show_window:` display google chrome's window.
    Returns:
        A google's webdriver.
    """
    options = webdriver.ChromeOptions()
    options.add_argument(f'user-data-dir=/home/{_username}/.config/google-chrome/{_profile}')

    if not show_window:
        options.add_argument('--headless')

    return webdriver.Chrome(options=options)