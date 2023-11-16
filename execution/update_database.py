from server.updaters.readm import (
    update_mangas_from_websites as update_mangas_from_readm,
)
from server.updaters.ler_manga import (
    update_mangas_from_websites as update_mangas_from_ler_manga,
)
from execution.log_configs import logger


def update_database(args):
    logger.info("Starting the site update process")

    website_list = args["website_to_update"]
    number_of_works = args["number_of_works"]
    exec_all = args["exec_all"]

    if "readm" in website_list:
        update_mangas_from_readm(number_of_works, exec_all)

    if "ler_manga" in website_list:
        update_mangas_from_ler_manga(number_of_works, exec_all)

    logger.info("Stoping the site update process")
