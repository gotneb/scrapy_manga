from server.updaters.create_threads_to_update_mangas import default_number_of_works
import argparse


def define_program_args():
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
        default=default_number_of_works,
        action="store",
        type=int,
        help=f"Set the number of threads to be executed during the website update (default: {default_number_of_works}).",
    )

    scheduled_time = 23

    parser.add_argument(
        "-s",
        "--schedule",
        default=scheduled_time,
        action="store",
        type=int,
        help=f"Schedule the program's execution time [value 0-23] (default: {scheduled_time}).",
        metavar="[0-23]",
        choices=range(0, 24),
    )

    parser.add_argument(
        "-a",
        "--all",
        action="store_true",
        help="Update all mangas from the source websites.",
    )

    return parser.parse_args()
