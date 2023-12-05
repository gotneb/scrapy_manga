from ...api.info.origin_info import get_origin_info, update_info

from entities import WebsiteUpdate

from ..create_threads_to_update_mangas import create_threads_to_update_mangas
from execution.log_configs import logger
from core.sites.nine_manga_br.constants import origin, language
from .upsert import upsert_manga
from .website_info import (
    get_all_urls,
    get_latest_updated_manga_urls,
    get_most_popular_manga_urls,
)


def update_mangas(number_of_works: int, exec_all: bool = False):
    """
    Updates manga from website.

    Args:
        number_of_works (int): Number of threads used for accessing the website.
        exec_all (bool): If True, updates all mangas from the website.

    Returns:
        None
    """

    logger.info(f"Updating mangas from {origin}.")

    try:
        # Update site information in database
        popular_urls = get_most_popular_manga_urls()

        # define if process all urls
        if exec_all:
            urls_for_update = get_all_urls()
        else:
            urls_for_update = get_latest_updated_manga_urls() + popular_urls

        # create threads
        create_threads_to_update_mangas(urls_for_update, upsert_manga, number_of_works)

        # update informations about mangas in the api
        if popular_urls:
            info = WebsiteUpdate(origin, popular_urls, language)
            update_info(info)

    except Exception as error:
        logger.critical(
            f"({origin}) on update mangas.",
            exc_info=True,
        )
