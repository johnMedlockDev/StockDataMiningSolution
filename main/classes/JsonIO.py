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
        self.oldJsonFilePath = ""

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
                Logger.LogInfo(
                    f"Successful JSON file creation of {symbol} in {eJsonFolder.value}!")
        except:
            Logger.LogError(f"Failure JSON file creation of {symbol}!")

    def RetrieveJsonFromFile(self, directory: str):
        """Loops over a directory and returns the symbol name and the json data.

        Args:
            directory (str): Name of the directory

        Returns:
            list (str, dict): [symbol, jsonData]
        """

        filenames = os.listdir(f"./io/json/{directory}")
        symbolAndJsonData = []
        for filename in filenames:
            if filename.endswith(".json"):
                symbolAndJsonData = self.OpenJsonFile(directory, filename)
                self.MoveJsonFile(self.oldJsonFilePath,
                                  directory, EJsonFolder.DONE, filename)
                break

        return symbolAndJsonData

    def OpenJsonFile(self, directory, filename):
        """Opens a Json file and returns the file name and JSON in an array.

        Args:
            directory (str): The current directory.
            filename (str): The full file name.

        Returns:
            [str, dict]: The filename and JSON dictionary.
        """

        self.oldJsonFilePath = f"{pathlib.Path().absolute()}\\io\\json\\{directory}\\{filename}"
        symbol = filename.replace('.json', "")
        try:
            with open(self.oldJsonFilePath) as jsonFile:
                jsonData = json.load(jsonFile)
            return [symbol, jsonData]
        except:
            Logger.LogError(f"Couldn't open file at {self.oldJsonFilePath}")
            return []

    def MoveJsonFile(self, oldJsonFilePath: str, directory: str, subdirectory: EJsonFolder, filename: str):
        """Moves a file in the json folder to another subfolder

        Args:
            oldJsonFilePath (str): The old file path.
            directory (str): The new target Directory
            subdirectory (EJsonFolder): The destination folder
            filename (str): The full file name.
        """
        newJsonFilePath = f"{pathlib.Path().absolute()}\\io\\json\\{directory}\\{subdirectory.value}\\{filename}"
        os.replace(oldJsonFilePath, newJsonFilePath)
        Logger.LogInfo(
            f" Moved file from {oldJsonFilePath} to {newJsonFilePath}")
