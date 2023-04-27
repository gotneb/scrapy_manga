from server import ReadmHandler, MangaDatabase, Database
import schedule
from time import sleep
from random import randomint


def update_sites():
    db = MangaDatabase()

    db.connect()

    handler = ReadmHandler(db)
    handler.start()
    handler.join()

    db.close()


if __name__ == "__main__":
    hour = 23
    minutes = randomint(0, 60)
    schedule.every().day.at("{:02d}:{:02d}".format(hour, minutes)).do(update_sites)

    while True:
        schedule.run_pending()
        sleep(60)
