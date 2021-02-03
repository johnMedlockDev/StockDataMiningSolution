from main.enums.EPayload import EPayload
from os import sys
from main.classes.AlphaAPIHandler import AlphaAPIHandler
from main.classes.SymbolListGenerator import SymbolListGenerator
from main.classes.Logger import Logger


class HistoricSymbolDataGenerator():
    """Generates repositories of Symbol data.

    Args:
        filename (str): 'symbols.csv'
        columnname (str, optional): Name of the column.
    """

    def __init__(self, filename: str, columnname: str = "SYMBOL") -> None:
        super().__init__()
        self.__filename = filename
        self.__columnname = columnname
        self.__logger = Logger()

    def GenerateJsonSymbolRepository(self, payload: EPayload = EPayload.FULL):
        """Generates a Json Repository from a list of tickers.

        Args:
            payload (EPayload, optional): EPayload decides how many much data will be returned. Defaults to EPayload.FULL.
        """

        self.__logger.LogInfo("Passing filtered symbols to AlphaAPIHandler.")

        filteredSymbols = self.RetrieveListOfFilteredSymbols()

        apiagent = AlphaAPIHandler()

        apiagent.GetHistoricalPriceDataFromJsonAPIAndWriteToJSONFileBatch(
            filteredSymbols, payload)

    def RetrieveListOfFilteredSymbols(self):
        """Retrieves a list of filtered symbols based off what is already with the Json repository.

        Returns:
            list: Filtered list of symbols.
        """

        self.__logger.LogInfo("Creating a filtered list of symbols.")

        symbolListGenerator = SymbolListGenerator(self.__filename)

        symbolListGenerator.CreateListOfSymbolsFromDataFrame(self.__columnname)

        filteredSymbolList = symbolListGenerator.CreateFilteredListOfSymbols()

        return filteredSymbolList
