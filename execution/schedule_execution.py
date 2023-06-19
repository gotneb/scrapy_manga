import schedule
from time import sleep
from random import randint
from datetime import datetime

from .update_database import update_database
from .log_configs import logger


def schedule_execution(hour: int, number_of_works: int, exec_all: bool = False):
    """Schedule the update for the specified time (but minutes is random)."""

    while True:
        # define update time
        time = "{:02d}:{:02d}".format(hour, randint(0, 60))

        # schedule udpate
        schedule.every().day.at(time).do(update_database, number_of_works, exec_all)
        next_task = schedule.jobs[0]

        logger.info(f"Scheduled update for {next_task.next_run}.")

        # wait for next task
        sleep_time = (next_task.next_run - datetime.now()).total_seconds()

        if sleep_time > 0:
            sleep(sleep_time)

        # execute pending tasks
        schedule.run_pending()

        # clear tasks
        schedule.clear()
