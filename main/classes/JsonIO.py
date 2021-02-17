from json import dump
import json
from main.enums.EJsonFolder import EJsonFolder
from pathlib import Path
from main.classes.Logger import Logger
import os


class JsonIO():

    def __init__(self) -> None:
        self.__oldJsonFilePath__ = ""

    def WriteJsonToFile(self, directory: EJsonFolder, filename: str, jsonObject: dict):

        try:
            with open(f'{Path().absolute()}\\io\\json\\{directory.value}\\{filename.upper()}.json', 'w') as outfile:
                dump(jsonObject, outfile)
                Logger.LogInfo(
                    f"Successful JSON file creation of {filename} in {directory.value}!")
        except:
            Logger.LogError(f"Failure JSON file creation of {filename}!")

    def ReadJsonFromFile(self, directory: EJsonFolder):

        filenames = os.listdir(f"./io/json/{directory.value}")
        symbolAndJsonData = []
        for filename in filenames:
            if filename.endswith(".json"):
                symbolAndJsonData = self.OpenJsonFile(
                    directory, filename)
                self.MoveJsonFile(directory,
                                  EJsonFolder.DONE, filename)
                break

        return symbolAndJsonData

    def OpenJsonFile(self, directory: EJsonFolder, filename: str):

        self.__oldJsonFilePath__ = f"{Path().absolute()}\\io\\json\\{directory.value}\\{filename}"
        symbol = filename.replace('.json', "")
        try:
            with open(self.__oldJsonFilePath__) as jsonFile:
                jsonData = json.load(jsonFile)
            return [symbol, jsonData]
        except:
            Logger.LogError(
                f"Couldn't open file at {self.__oldJsonFilePath__}")
            return []

    def MoveJsonFile(self, directory: EJsonFolder, subDirectory: EJsonFolder, filename: str):

        newJsonFilePath = f"{Path().absolute()}\\io\\json\\{directory.value}\\{subDirectory.value}\\{filename}"
        os.replace(self.__oldJsonFilePath__, newJsonFilePath)
        Logger.LogInfo(
            f" Moved file from {self.__oldJsonFilePath__} to {newJsonFilePath}")
