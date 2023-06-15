from server.updaters.readm import update_mangas as readm_update_mangas
from server.updaters.golden_mangas import update_mangas as golden_mangas_update_mangas
from server.updaters.create_threads_to_update_mangas import number_of_works

import schedule
from time import sleep
from random import randint
import argparse


def update_database(exec_all: bool = False):
    readm_update_mangas(exec_all)
    golden_mangas_update_mangas(exec_all)


if __name__ == "__main__":
    # Handling program arguments
    parser = argparse.ArgumentParser(description="Arguments for website update")

    parser.add_argument(
        "-n",
        "--now",
        action="store_true",
        help="Update websites immediately upon program invocation and then exit.",
    )

    parser.add_argument(
        "-t",
        "--threads",
        default=number_of_works,
        action="store",
        type=int,
        help=f"Set the number of threads to be executed during the website update (default: {number_of_works}).",
    )

    parser.add_argument(
        "-a",
        "--all",
        action="store_true",
        help="Update all mangas from the source websites.",
    )

    args = parser.parse_args()

    # define number of threads
    if args.threads:
        number_of_works = args.threads

    exec_all = False

    if args.all:
        exec_all = True

    # run now and finish
    if args.now:
        update_database(exec_all)
    else:
        # schedule execution
        hour = 23
        minutes = randint(0, 60)
        schedule.every().day.at("{:02d}:{:02d}".format(hour, minutes)).do(
            update_database, exec_all
        )

        while True:
            schedule.run_pending()
            sleep(10 * 60)  # checks every 10 minutes
