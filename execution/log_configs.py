import logging

log_file_name = "exec_logs.log"

# create and configure logger
logging.basicConfig(
    filename=log_file_name, format="%(asctime)s %(message)s", filemode="w"
)

logger = logging.getLogger()

# set the threshold of logger
logger.setLevel(logging.INFO)
