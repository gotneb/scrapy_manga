from server.updaters.create_threads_to_update_mangas import number_of_works
from execution.define_program_args import define_program_args
from execution.update_database import update_database
from execution.schedule_execution import schedule_execution

if __name__ == "__main__":
    # Handling program arguments
    args = define_program_args()

    # define number of threads
    number_of_works = args.threads

    # run now and finish
    if args.now:
        update_database(args.all)
    else:  # schedule execution
        schedule_execution(args.schedule, args.all)
