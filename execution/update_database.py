from server.updaters.readm import (
    update_mangas_from_websites as update_mangas_from_readm,
)
from server.updaters.golden_mangas import (
    update_mangas_from_websites as update_mangas_from_golden,
)
from execution.log_configs import logger


def update_database(number_of_works: int, exec_all: bool = False):
    logger.info("Starting the site update process")

    update_mangas_from_readm(number_of_works, exec_all)
    update_mangas_from_golden(number_of_works, exec_all)

    logger.info("Stoping the site update process")
