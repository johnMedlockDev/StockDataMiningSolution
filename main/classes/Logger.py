import logging
from datetime import date


class Logger():
    """This is the project logger, you can output 3 types of log to the log file. (INFO, ERROR, DEBUG)

    """

    def __init__(self) -> None:
        pass

    @staticmethod
    def LogError(message: str):
        """Persist a ERROR to a log file

        Args:
            message (str): 'File doesn't exist'
        """
        logging.basicConfig(filename=f"io/logs/{date.today()}.log",
                            format='%(asctime)s %(message)s',
                            filemode='a', level=logging.DEBUG)
        logging.getLogger().error(f"ERROR: {message}")

    @staticmethod
    def LogInfo(message: str):
        """Persist a INFO to a log file

        Args:
            message (str): 'This is some more info about this function.'
        """
        logging.basicConfig(filename=f"io/logs/{date.today()}.log",
                            format='%(asctime)s %(message)s',
                            filemode='a', level=logging.DEBUG)
        logging.getLogger().info(f"INFO: {message}")

    @staticmethod
    def LogDebug(message: str):
        """Persist a DEBUG message to a log file

        Args:
            message (str): 'This is why this thing broke.'
        """
        logging.basicConfig(filename=f"io/logs/{date.today()}.log",
                            format='%(asctime)s %(message)s',
                            filemode='a', level=logging.DEBUG)
        logging.getLogger().debug(f"DEBUG: {message}")
