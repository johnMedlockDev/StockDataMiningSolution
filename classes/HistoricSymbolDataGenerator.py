from classes.enums.EPayload import EPayload
from os import sys
from classes.AlphaAPIHandler import AlphaAPIHandler
from classes.SymbolListGenerator import SymbolListGenerator
from classes.Logger import Logger


class HistoricSymbolDataGenerator():
    """Generates repositories of Symbol data.

    """

    def __init__(self, filename: str, columnname: str = "SYMBOL") -> None:
        super().__init__()
        self.filename = filename
        self.columnname = columnname
        self.logger = Logger()

    def GenerateJsonSymbolRepository(self, payload: EPayload = EPayload.FULL):
        """Generates a Json Repository from a list of tickers.

        Args:
            payload (EPayload, optional): EPayload decides how many much data will be returned. Defaults to EPayload.FULL.
        """

        self.logger.LogInfo("Passing filtered symbols to AlphaAPIHandler.")

        filteredSymbols = self.RetrieveListOfFilteredSymbols()

        apiagent = AlphaAPIHandler()

        apiagent.GetHistoricalPriceDataFromJsonAPIAndWriteToJSONFileBatch(
            filteredSymbols, payload)

    def RetrieveListOfFilteredSymbols(self):
        """Retrieves a list of filtered symbols based off what is already with the Json repository.

        Returns:
            list: Filtered list of symbols.
        """

        self.logger.LogInfo("Creating a filtered list of symbols.")

        symbolListGenerator = SymbolListGenerator(self.filename)

        symbolListGenerator.CreateListOfSymbolsFromDataFrame(self.columnname)

        filteredSymbolList = symbolListGenerator.CreateFilteredListOfSymbols()

        return filteredSymbolList
