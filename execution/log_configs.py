import logging
import os

log_file_name = "exec_logs.log"
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)

log_file_path = os.path.join(parent_dir, log_file_name)

# create and configure logger
logging.basicConfig(
    filename=log_file_path, format="%(asctime)s %(message)s", filemode="w"
)

logger = logging.getLogger()

# set the threshold of logger
logger.setLevel(logging.INFO)
