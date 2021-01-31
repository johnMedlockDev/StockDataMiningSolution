import pandas
import pathlib
from classes.Logger import Logger


class SymbolListGenerator(object):
    """
    Creates a Pandas Dataframe out of a CSV located in the io\csvs\source\ directory.
    :param: filename = "symbols.csv"

    """

    def __init__(self, filename: str):
        self.__FILENAME = f'{pathlib.Path().absolute()}\\io\\csvs\\source\\{filename}'
        self.__DFList = []
        self.__DF = pandas.read_csv(self.__FILENAME)
        self.logger = Logger()

    def CreateListFromDataFrame(self, columnname: str):
        '''
        Creates a list from a dataframe column.
        :param: columnname = 'SYMBOL' 

        '''
        self.__DFList = self.__DF[columnname].to_list()

    def GetListFromDataFrame(self):
        '''
        Retrieves the list that was created from a dataframe column.

        '''
        return self.__DFList
