import logging
import os

# directory paths
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)

# file paths

# create and configure main logger
msg_format = "%(asctime)s %(levelname)s %(message)s "
formater = logging.Formatter(msg_format)

# main logger configs
debug_log_file_path = os.path.join(parent_dir, "debug_logs.log")
logging.basicConfig(
    filename=debug_log_file_path, format=msg_format, filemode="w", level=logging.DEBUG
)
logger = logging.getLogger(debug_log_file_path)

# info logger configs
info_log_file_path = os.path.join(parent_dir, "info_logs.log")
info_logger_handler = logging.FileHandler(filename=info_log_file_path, mode="w")
info_logger_handler.setLevel(logging.INFO)
info_logger_handler.setFormatter(formater)

info_filter = logging.Filter()
info_filter.filter = lambda record: record.levelno == logging.INFO
info_logger_handler.addFilter(info_filter)

# error logger configs
error_log_file_path = os.path.join(parent_dir, "error_logs.log")
error_logger_handler = logging.FileHandler(filename=error_log_file_path, mode="w")
error_logger_handler.setLevel(logging.WARNING)
error_logger_handler.setFormatter(formater)

# add handlers in main logger
logger.addHandler(info_logger_handler)
logger.addHandler(error_logger_handler)
