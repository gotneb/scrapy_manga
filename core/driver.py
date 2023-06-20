from selenium import webdriver

_profile = 'selenium_manga'

def init_driver(show_window) -> webdriver.Chrome:
    """
    Creates a webdriver.\n
    Arguments:  
        `show_window:` display google chrome's window.
    Returns:
        A google's webdriver.
    """
    options = webdriver.ChromeOptions()
    options.add_argument(f"user-data-dir=/home/gabriel/.config/google-chrome/{_profile}")

    if not show_window:
        options.add_argument('--headless')

    return webdriver.Chrome(options=options)