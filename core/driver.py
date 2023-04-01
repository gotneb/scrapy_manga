from selenium import webdriver

def init_driver(show_window) -> webdriver.Chrome:
    """
    Creates a webdriver.\n
    Arguments:  
        `show_window:` display google chrome's window.
    Returns:
        A google's webdriver.
    """
    # TODO: Throw exception if chrome is not installed
    if not show_window:
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        #options.add_argument('--no-sandbox')
        #options.add_argument('--disable-dev-shm-usage')
        return webdriver.Chrome(options=options)
    else:
        return webdriver.Chrome()