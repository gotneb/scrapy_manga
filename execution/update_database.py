from server.updaters.readm.update_mangas import (
    update_mangas as update_mangas_from_readm,
)
from server.updaters.nine_manga_br.update_mangas import (
    update_mangas as update_mangas_nine,
)
from execution.log_configs import logger


def update_database(args):
    logger.info("Starting the site update process")

    website_list = args["website_to_update"]
    number_of_works = args["number_of_works"]
    exec_all = args["exec_all"]

    if "nine_manga_br" in website_list:
        update_mangas_nine(number_of_works, exec_all)

    if "readm" in website_list:
        update_mangas_from_readm(number_of_works, exec_all)

    logger.info("Stoping the site update process")
