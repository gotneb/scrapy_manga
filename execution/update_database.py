from server.updaters.readm import update_mangas as readm_update_mangas
from server.updaters.golden_mangas import update_mangas as golden_mangas_update_mangas
from execution.log_configs import logger


def update_database(number_of_works: int, exec_all: bool = False):
    logger.info("Starting the website update process\n")

    logger.info("\nUpdating readm.org\n")
    readm_update_mangas(number_of_works, exec_all)

    logger.info("\nUpdating goldenmangas.top\n")
    golden_mangas_update_mangas(number_of_works, exec_all)
