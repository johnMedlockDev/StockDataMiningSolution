from tkinter.filedialog import Directory
from main.enums.EJsonFolder import EJsonFolder
import pandas
import pathlib
from main.classes.Logger import Logger
from os import listdir
from os.path import isfile, join


class SymbolListGenerator():

    def __init__(self, fileName: str, columnName: str):
        self.__DF__ = pandas.read_csv(
            f'{pathlib.Path().absolute()}\\io\\csv\\source\\{fileName}')[columnName].to_list()
        self.__parentDirectory__ = ''
        self.__childDirectory__ = ''

    def CreateFilteredListOfSymbols(self, eJsonFolders:  list(EJsonFolder)):

        try:
            self.__parentDirectory__, self.__childDirectory__ = eJsonFolders
        except ValueError:
            self.__parentDirectory__ = eJsonFolders[0]
            self.__childDirectory__ = EJsonFolder.NONE

        listOfSymbolsThatAlreadyExist = self.GetAlreadyPersistedOfSymbols()

        listOfSymbols = self.__DF__
        if self.__childDirectory__ == EJsonFolder.REDO:
            return listOfSymbolsThatAlreadyExist
        else:
            for symbol in listOfSymbolsThatAlreadyExist:
                if symbol in listOfSymbols:
                    listOfSymbols.remove(symbol)

        return listOfSymbols

    def GetAlreadyPersistedOfSymbols(self):

        jsonPath = f"{pathlib.Path().absolute()}\\io\\json\\{self.__parentDirectory__.value}"

        if self.__childDirectory__.value != "":
            jsonPath = f"{jsonPath}\\{self.__childDirectory__.value}"

        files = [f.replace('.json', '') for f in listdir(
            jsonPath) if isfile(join(jsonPath, f))]

        return files
