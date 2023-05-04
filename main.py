from server import ReadmHandler, MangaDatabase, MangaLivreHandler
import schedule
from time import sleep
from random import randint
from dotenv import load_dotenv
from os import getenv

load_dotenv()


def update_database():
    db = MangaDatabase()

    if db.connect(getenv("MONGO_URI")):
        readmHandler = ReadmHandler(db)
        readmHandler.start()
        readmHandler.join()

        mangaLivreHandler = MangaLivreHandler(db)
        mangaLivreHandler.start()
        mangaLivreHandler.join()

        db.close()


if __name__ == "__main__":
    hour = 23
    minutes = randint(0, 60)
    schedule.every().day.at("{:02d}:{:02d}".format(hour, minutes)).do(update_database)

    while True:
        schedule.run_pending()
        sleep(10 * 60)  # checks every 10 minutes
