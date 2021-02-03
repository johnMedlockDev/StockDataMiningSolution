import pandas
import pathlib
from main.classes.Logger import Logger
from os import listdir
from os.path import isfile, join


class SymbolListGenerator():
    """Creates a Pandas Dataframe out of a CSV located in the io\csv\source\ directory.

    Args:
        filename (str): 'symbols.csv'
    """

    def __init__(self, filename: str):
        self.__FILENAME = f'{pathlib.Path().absolute()}\\io\\csv\\source\\{filename}'
        self.__DFList = []
        self.__DF = pandas.read_csv(self.__FILENAME)
        self.__logger = Logger()

    def CreateListOfSymbolsFromDataFrame(self, columnname: str):
        """Creates a list from a dataframe column.

        Args:
            columnname (str): 'SYMBOL'
        """
        self.__DFList = self.__DF[columnname].to_list()

    def GetListOfSymbolsFromDataFrame(self):
        """Retrieves the list that was created from a dataframe column.

        Returns:
            list: Symbol List of strings. 
        """
        return self.__DFList

    def GetAlreadyPersistedOfSymbols(self):
        """Retrieves a list of symbols already persisted to the json folder.

        Returns:
            list: Symbol List of strings. 
        """
        jsonPath = f"{pathlib.Path().absolute()}\\io\\json\\"

        files = [f.replace('.json', '') for f in listdir(
            jsonPath) if isfile(join(jsonPath, f))]

        return files

    def CreateFilteredListOfSymbols(self):
        """Creates a list of symbols - the symbols you already have in the Json folder.

        Returns:
            list: Symbol List of filtered strings. 
        """

        listOfSymbolsThatAlreadyExist = self.GetAlreadyPersistedOfSymbols()
        listOfSymbolsRaw = self.__DFList

        for symbolE in listOfSymbolsThatAlreadyExist:
            if symbolE in listOfSymbolsRaw:
                listOfSymbolsRaw.remove(symbolE)

        listOfSymbolsFiltered = [symbol for symbol in listOfSymbolsRaw]

        return listOfSymbolsFiltered
