from core.sites.nine_manga_br.latest import get_latest_updates
from core.sites.nine_manga_br.populars import get_populars
from core.sites.nine_manga_br.all_by_index import get_all_by_index, MAX_INDEX

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

    for index in range(1, MAX_INDEX):
        try:
            urls = urls + get_all_by_index(index=index)
        except Exception as error:
            logger.critical(
                f"({origin}) error getting all URLs (index={index}).",
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
