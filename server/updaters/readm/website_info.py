from core.sites.readm import get_latest_updates, get_populars, get_all_start_with

from .constants import origin
from execution.log_configs import logger


def get_all_urls() -> list[str]:
    """
    Retrieves all URLs from the website and returns them in alphabetical order.

    Returns:
        list[str]: A list of URLs sorted in alphabetical order.
    """
    logger.info(f"({origin}): downloading all mangas URLs.")
    urls = []

    for letter in [chr(i) for i in range(97, 123)]:
        try:
            urls = urls + get_all_start_with(letter=letter)
        except Exception as error:
            logger.critical(
                f"({origin}) error getting all URLs (letter={letter}).",
                exc_info=True,
            )

    return urls


def get_latest_updated_manga_urls() -> list[dict]:
    """
    Retrieves URLs of mangas that were most recently updated on the website.

    Returns:
        list[str]: A list of URLs of the latest updated mangas.
    """
    logger.info(f"({origin}): downloading updated mangas URLs.")
    manga_urls = []

    try:
        # get manga urls from chapters updates
        manga_urls += get_latest_updates(limit=400)

        manga_urls.reverse()
    except Exception as error:
        logger.critical(
            f"({origin}) error getting latest updated URLs.",
            exc_info=True,
        )

    return manga_urls


def get_most_popular_manga_urls() -> list[str]:
    """
    Retrieves URLs of the most popular mangas from the website.

    Returns:
        list[str]: A list of URLs of the most popular mangas.
    """
    logger.info(f"({origin}): downloading popular mangas URLs.")
    urls = []

    try:
        urls = get_populars()
    except Exception as error:
        logger.critical(
            f"({origin}) error getting populars URLs.",
            exc_info=True,
        )

    return urls
