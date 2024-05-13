import logging
import os
import sys
from datetime import datetime

from colorama import Fore, Style


class ColoredFormatter(logging.Formatter):
    FORMATS = {
        logging.DEBUG: Style.DIM + '%(asctime)s - %(levelname)s - %(message)s' + Style.RESET_ALL,
        logging.INFO: Fore.GREEN + '%(asctime)s - %(levelname)s - %(message)s' + Style.RESET_ALL,
        logging.WARNING: Fore.YELLOW + '%(asctime)s - %(levelname)s - %(message)s' + Style.RESET_ALL,
        logging.ERROR: Fore.RED + '%(asctime)s - %(levelname)s - %(message)s' + Style.RESET_ALL,
        logging.CRITICAL: Fore.RED + Style.BRIGHT + '%(asctime)s - %(levelname)s - %(message)s' + Style.RESET_ALL
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


class Log:
    def __init__(self, log_level=logging.INFO, print_log=True):
        self.log_file_path = self._get_log_file_path()
        self.log_level = log_level
        self._setup_logger()
        self._print_log = print_log

    def _setup_logger(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(self.log_level)
        self.logger.propagate = False

        self.file_handler = logging.FileHandler(self.log_file_path)
        self.file_handler.setLevel(logging.INFO)

        file_handler_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        self.file_handler.setFormatter(file_handler_formatter)

        # Create a stream handler to print log messages to the console
        self.stream_handler = logging.StreamHandler(sys.stdout)
        self.stream_handler.setLevel(logging.INFO)

        # Create formatters for both handlers
        stream_formatter = ColoredFormatter()
        self.stream_handler.setFormatter(stream_formatter)

        # Add both handlers to the logger
        self.logger.addHandler(self.file_handler)
        self.logger.addHandler(self.stream_handler)

        # # create console handler with a higher log level
        # ch = logging.StreamHandler(self.log_stream)
        # ch.setLevel(logging.INFO)

        # Create a formatter and set it for the console handler

        # ch.setFormatter(formatter)

        # logger.addHandler(self.file_handler)

    def set_print_log(self, print_log_value):
        self._print_log = print_log_value

    @staticmethod
    def _get_log_file_path():
        assigment_dir_path = os.getcwd()
        log_dir_path = os.path.join(assigment_dir_path, 'support_files', 'logging_directory')

        os.chmod(log_dir_path, 0o777)  # Set permissions to allow read, write, and execute for all users

        # Modify permissions if needed (e.g., make the directory writable)
        current_datetime = datetime.now()
        date_time_string = current_datetime.strftime('%Y_%m_%d_%H_%M_%S')
        if not os.path.exists(log_dir_path):
            os.makedirs(log_dir_path)
        log_file_path = os.path.join(log_dir_path, f"{date_time_string}.log")
        with open(log_file_path, "w"):
            pass
        return log_file_path

    def info(self, message):
        self.logger.info(message)

    def warning(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)

    def flush_logs(self):
        self.file_handler.flush()
        self.file_handler.close()
