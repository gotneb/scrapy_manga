from core.sites.readm import get_manga, get_populars
import logging, time

if __name__ == "__main__":
    ONE_MINUTE = 60
    logging.info("STARTING...")
    while True:
        manga = get_manga("https://readm.org/manga/versatile-mage")
        manga.show()
        time.sleep(2 * ONE_MINUTE)