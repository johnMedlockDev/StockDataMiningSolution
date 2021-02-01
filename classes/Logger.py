import logging
from datetime import date


class Logger(object):
    '''
    This is the project logger.
    You can output 3 types of log to the log file.
    - INFO
    - ERROR
    - DEBUG
    '''

    def __init__(self) -> None:
        super().__init__()
        logging.basicConfig(filename=f"io/logs/{date.today()}.log",
                            format='%(asctime)s %(message)s',
                            filemode='a', level=logging.INFO)
        self.logger = logging.getLogger()

    def LogError(self, message: str):
        self.logger.error(f"ERROR: {message}")

    def LogInfo(self, message: str):
        self.logger.info(f"INFO: {message}")

    def LogDebug(self, message: str):
        self.logger.debug(f"DEBUG: {message}")