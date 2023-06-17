import schedule
from time import sleep
from random import randint
from datetime import datetime

from .update_database import update_database
from execution.log_configs import logger


def schedule_execution(hour: int, number_of_works: int, exec_all: bool = False):
    minutes = randint(0, 60)
    time = "{:02d}:{:02d}".format(hour, minutes)

    logger.info(f"Scheduled update for every day at {time}.")

    schedule.every().day.at(time).do(update_database, number_of_works, exec_all)

    while True:
        schedule.run_pending()
        next_task = schedule.next_run()
        sleep_time = (next_task - datetime.now()).total_seconds()

        if sleep_time > 0:
            sleep(sleep_time)
