from json import dump
import pathlib
from main.classes.Logger import Logger


class JsonIO():
    """Write Json to file based of symbol name.
    
    """

    def __init__(self) -> None:
        super().__init__()
        self.__logger = Logger()

    def WriteJsonToFile(self, symbol: str, jsonObject: dict):
        """Writes Json to file based of symbol name.

        Args:
            symbol (str): symbol = 'IBM'
            jsonObject (dict): jsonObject = {"2021-01-29": {"1. open": "25.1600", "2. high": "25.1600", "3. low": "25.1450", "4. close": "25.1450", "5. volume": "3099"}
        """
        try:
            with open(f'{pathlib.Path().absolute()}\\io\\json\\{symbol.upper()}.json', 'w') as outfile:
                dump(jsonObject, outfile)
                self.__logger.LogInfo(
                    f"Successful JSON file creation of {symbol}!")
        except:
            self.__logger.LogError(f"Failure JSON file creation of {symbol}!")
