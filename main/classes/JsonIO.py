from json import dump
import json
from main.enums.EJsonFolder import EJsonFolder
import pathlib
from main.classes.Logger import Logger
import os


class JsonIO():
    """Write Json to file based of symbol name.

    """

    def __init__(self) -> None:
        super().__init__()
        self.__logger = Logger()

    def WriteJsonToFile(self, symbol: str, eJsonFolder: EJsonFolder, jsonObject: dict):
        """Writes Json to file based of symbol name.

        Args:
            symbol (str): symbol = 'IBM'
            folder (str): folder = 'subfolder in json folder'
            jsonObject (dict): jsonObject = {"2021-01-29": {"1. open": "25.1600", "2. high": "25.1600", "3. low": "25.1450", "4. close": "25.1450", "5. volume": "3099"}
        """
        try:
            with open(f'{pathlib.Path().absolute()}\\io\\json\\{eJsonFolder.value}\\{symbol.upper()}.json', 'w') as outfile:
                dump(jsonObject, outfile)
                self.__logger.LogInfo(
                    f"Successful JSON file creation of {symbol} in {eJsonFolder.value}!")
        except:
            self.__logger.LogError(f"Failure JSON file creation of {symbol}!")

    def RetrieveJsonFromFile(self, directory: str):
        """Loops over a directory and returns the symbol name and the json data.

        Args:
            directory (str): Name of the directory

        Returns:
            list (str, dict): [symbol, jsonData]
        """

        entries = os.listdir(f"./io/json/{directory}")
        jsonData = {}
        symbol = ""
        for entry in entries:
            if entry.endswith(".json"):
                jsonFilePath = f"{pathlib.Path().absolute()}\\io\\json\\{directory}\\{entry}"
                symbol = entry.replace('.json', "")
                with open(jsonFilePath) as jsonFile:
                    jsonData = json.load(jsonFile)

                print(jsonData)

                newJsonFilePath = f"{pathlib.Path().absolute()}\\io\\json\\{directory}\\done\\{entry}"
                os.replace(jsonFilePath, newJsonFilePath)
                break

        return [symbol, jsonData]
