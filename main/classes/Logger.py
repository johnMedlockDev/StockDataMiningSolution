import logging
from datetime import date


class Logger():
    """This is the project logger, you can output 3 types of log to the log file. (INFO, ERROR, DEBUG)

    """

    def __init__(self) -> None:
        super().__init__()
        logging.basicConfig(filename=f"io/logs/{date.today()}.log",
                            format='%(asctime)s %(message)s',
                            filemode='a', level=logging.DEBUG)
        self.__logger = logging.getLogger()

    def LogError(self, message: str):
        """Persist a ERROR to a log file

        Args:
            message (str): 'File doesn't exist'
        """
        self.__logger.error(f"ERROR: {message}")

    def LogInfo(self, message: str):
        """Persist a INFO to a log file

        Args:
            message (str): 'This is some more info about this function.'
        """
        self.__logger.info(f"INFO: {message}")

    def LogDebug(self, message: str):
        """Persist a DEBUG message to a log file

        Args:
            message (str): 'This is why this thing broke.'
        """
        self.__logger.debug(f"DEBUG: {message}")
