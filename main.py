from server.updaters.readm import update_mangas as readm_update_mangas
from server.updaters.golden_mangas import update_mangas as golden_mangas_update_mangas

import schedule
from time import sleep
from random import randint


def update_database():
    readm_update_mangas()
    golden_mangas_update_mangas()


if __name__ == "__main__":
    hour = 23
    minutes = randint(0, 60)
    schedule.every().day.at("{:02d}:{:02d}".format(hour, minutes)).do(update_database)

    while True:
        schedule.run_pending()
        sleep(10 * 60)  # checks every 10 minutes
