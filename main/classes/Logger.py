import logging
from datetime import date


class Logger():

    @staticmethod
    def LogError(message: str):

        logging.basicConfig(filename=f"io/logs/{date.today()}.log",
                            format='%(asctime)s %(message)s',
                            filemode='a', level=logging.DEBUG)
        logging.getLogger().error(f"ERROR: {message}")

    @staticmethod
    def LogInfo(message: str):

        logging.basicConfig(filename=f"io/logs/{date.today()}.log",
                            format='%(asctime)s %(message)s',
                            filemode='a', level=logging.DEBUG)
        logging.getLogger().info(f"INFO: {message}")

    @staticmethod
    def LogDebug(message: str):

        logging.basicConfig(filename=f"io/logs/{date.today()}.log",
                            format='%(asctime)s %(message)s',
                            filemode='a', level=logging.DEBUG)
        logging.getLogger().debug(f"DEBUG: {message}")
