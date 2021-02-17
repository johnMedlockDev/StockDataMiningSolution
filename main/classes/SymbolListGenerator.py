import os
from main.enums.EJsonFolder import EJsonFolder
from pandas import read_csv
from pathlib import Path
from main.classes.Logger import Logger
from os import listdir
from os.path import isfile, join


class SymbolListGenerator():

    def __init__(self, fileName: str, columnName: str):
        self.__DF__ = read_csv(
            f'{Path().absolute()}\\io\\csv\\source\\{fileName}.csv')[columnName].to_list()
        self.__parentDirectory__ = ''
        self.__childDirectory__ = ''

    def CreateFilteredListOfSymbols(self, directories: list(EJsonFolder)):

        try:
            self.__parentDirectory__, self.__childDirectory__ = directories
        except ValueError:
            self.__parentDirectory__ = directories[0]
            self.__childDirectory__ = EJsonFolder.NONE

        listOfExistingSymbols = self.GetPersistedOfSymbols()

        listOfSymbols = self.__DF__
        if self.__childDirectory__ == EJsonFolder.REDO:
            return self.FliterRedoList(listOfExistingSymbols)

        for symbol in listOfExistingSymbols:
            if symbol in listOfSymbols:
                listOfSymbols.remove(symbol)
        return listOfSymbols

    def GetPersistedOfSymbols(self):

        jsonPath = f"{Path().absolute()}\\io\\json\\{self.__parentDirectory__.value}"

        listOfPersistedSymbols = []

        symbolsInParent = [f.replace('.json', '') for f in listdir(
            jsonPath) if isfile(join(jsonPath, f))]

        symbolsInDone = []

        if self.__childDirectory__.value == EJsonFolder.REDO.value:
            jsonPath = f"{jsonPath}\\{EJsonFolder.DONE.value}"

            symbolsInDone = [f.replace('.json', '') for f in listdir(
                jsonPath) if isfile(join(jsonPath, f))]

        listOfPersistedSymbols = list(set(symbolsInParent+symbolsInDone))

        return listOfPersistedSymbols

    def FliterRedoList(self, listOfPersistedSymbols: list):
        jsonPath = f"{Path().absolute()}\\io\\json\\{self.__parentDirectory__.value}\\{EJsonFolder.REDO.value}"

        filesInRedoFolder = [f.replace('.json', '') for f in listdir(
            jsonPath) if isfile(join(jsonPath, f))]

        for file in listOfPersistedSymbols:
            if file in filesInRedoFolder:
                filesInRedoFolder.remove(file)
                Logger.LogInfo(
                    f"Removed file {file}.json from {self.__parentDirectory__.value}\{EJsonFolder.REDO.value} because it already exist in {self.__parentDirectory__.value}\done.")
                os.remove(f"{jsonPath}\\{file}.json")
        return filesInRedoFolder
