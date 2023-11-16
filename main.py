from execution.program_args import get_program_args
from execution.update_database import update_database
from execution.schedule_execution import schedule_execution

if __name__ == "__main__":
    # Handling program arguments
    args = get_program_args()

    # if is not null, schedule execution
    if args["schedule"]:
        schedule_execution(args)
    else:
        update_database(args)
