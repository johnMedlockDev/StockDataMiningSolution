from json import dump
import json
from main.enums.EJsonFolder import EJsonFolder
import pathlib
from main.classes.Logger import Logger
import os


class JsonIO():

    def __init__(self) -> None:
        super().__init__()
        self.__oldJsonFilePath__ = ""

    def WriteJsonToFile(self, symbol: str, eJsonFolder: EJsonFolder, jsonObject: dict):

        try:
            with open(f'{pathlib.Path().absolute()}\\io\\json\\{eJsonFolder.value}\\{symbol.upper()}.json', 'w') as outfile:
                dump(jsonObject, outfile)
                Logger.LogInfo(
                    f"Successful JSON file creation of {symbol} in {eJsonFolder.value}!")
        except:
            Logger.LogError(f"Failure JSON file creation of {symbol}!")

    def ReadJsonFromFile(self, eJsonFolder: EJsonFolder):

        filenames = os.listdir(f"./io/json/{eJsonFolder.value}")
        symbolAndJsonData = []
        for filename in filenames:
            if filename.endswith(".json"):
                symbolAndJsonData = self.OpenJsonFile(
                    eJsonFolder, filename)
                self.MoveJsonFile(eJsonFolder,
                                  EJsonFolder.DONE, filename)
                break

        return symbolAndJsonData

    def OpenJsonFile(self, eJsonFolder: EJsonFolder, filename: str):

        self.__oldJsonFilePath__ = f"{pathlib.Path().absolute()}\\io\\json\\{eJsonFolder.value}\\{filename}"
        symbol = filename.replace('.json', "")
        try:
            with open(self.__oldJsonFilePath__) as jsonFile:
                jsonData = json.load(jsonFile)
            return [symbol, jsonData]
        except:
            Logger.LogError(
                f"Couldn't open file at {self.__oldJsonFilePath__}")
            return []

    def MoveJsonFile(self, eJsonFolder1: EJsonFolder, eJsonFolder2: EJsonFolder, filename: str):

        newJsonFilePath = f"{pathlib.Path().absolute()}\\io\\json\\{eJsonFolder1.value}\\{eJsonFolder2.value}\\{filename}"
        os.replace(self.__oldJsonFilePath__, newJsonFilePath)
        Logger.LogInfo(
            f" Moved file from {self.__oldJsonFilePath__} to {newJsonFilePath}")
