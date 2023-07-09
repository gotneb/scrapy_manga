from execution.define_program_args import define_program_args
from execution.update_database import update_database
from execution.schedule_execution import schedule_execution

if __name__ == "__main__":
    # Handling program arguments
    args = define_program_args()

    # run now and finish
    if args.now:
        update_database(args.threads, args.all)
    else:  # schedule execution
        schedule_execution(args.schedule, args.threads, args.all)
