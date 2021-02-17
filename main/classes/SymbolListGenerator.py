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

        self.InitializeDirectories(directories)

        listOfPersistedSymbols = self.GetListPersistedOfSymbols()

        listOfSymbols = self.__DF__

        if self.__childDirectory__ == EJsonFolder.REDO:
            return self.FliterRedoList(listOfPersistedSymbols)

        for symbol in listOfPersistedSymbols:
            if symbol in listOfSymbols:
                listOfSymbols.remove(symbol)
                
        return listOfSymbols

    def InitializeDirectories(self, directories: list(EJsonFolder)):
        try:
            self.__parentDirectory__, self.__childDirectory__ = directories
        except ValueError:
            self.__parentDirectory__ = directories[0]
            self.__childDirectory__ = EJsonFolder.NONE

    def GetListPersistedOfSymbols(self):

        listOfPersistedSymbols = list(
            set(self.GetListFromParentDirectory()+self.GetListFromDoneDirectory()))

        return listOfPersistedSymbols

    def GetListFromParentDirectory(self):
        jsonPath = f"{self.GetParentPath()}"
        return [f.replace('.json', '') for f in listdir(jsonPath) if isfile(join(jsonPath, f))]

    def GetListFromDoneDirectory(self):
        jsonPath = f"{self.GetParentPath()}\{EJsonFolder.DONE.value}"
        return [f.replace('.json', '') for f in listdir(
            jsonPath) if isfile(join(jsonPath, f))]

    def FliterRedoList(self, listOfPersistedSymbols: list):
        jsonPath = f"{self.GetParentPath()}\{EJsonFolder.REDO.value}"
        filesInRedoFolder = self.GetListFromRedoDirectory()

        for file in listOfPersistedSymbols:
            if file in filesInRedoFolder:
                filesInRedoFolder.remove(file)
                Logger.LogInfo(
                    f"Removed file {file}.json from {self.__parentDirectory__.value}\\redo because it already exist in {self.__parentDirectory__.value}\\done.")
                os.remove(f"{jsonPath}\\{file}.json")
        return filesInRedoFolder

    def GetListFromRedoDirectory(self):
        jsonPath = f"{self.GetParentPath()}\\{EJsonFolder.REDO.value}"
        return [f.replace('.json', '') for f in listdir(
            jsonPath) if isfile(join(jsonPath, f))]

    def GetParentPath(self):
        return f"{Path().absolute()}\io\json\{self.__parentDirectory__.value}"
