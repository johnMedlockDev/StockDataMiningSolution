from main.classes.SQLIO import SQLIO
from main.enums.ERepositoryAction import ERepositoryAction
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

    def GenerateJsonSymbolPriceRepository(self, payload: EPayload = EPayload.FULL):
        """Generates a Json Repository from a list of tickers.

        Args:
            payload (EPayload, optional): EPayload decides how many much data will be returned. Defaults to EPayload.FULL.
        """

        Logger.LogInfo("Passing filtered symbols to AlphaAPIHandler.")

        filteredSymbols = self.RetrieveListOfFilteredSymbols(
            ERepositoryAction.PRICES)

        apiagent = AlphaAPIHandler()

        apiagent.GetHistoricalPriceDataFromJsonAPIAndWriteToJSONFileBatch(
            filteredSymbols, payload)

    def GenerateJsonSymbolEarningsRepository(self, payload: EPayload = EPayload.FULL):
        """Generates a Json Repository from a list of tickers.

        Args:
            payload (EPayload, optional): EPayload decides how many much data will be returned. Defaults to EPayload.FULL.
        """

        Logger.LogInfo("Passing filtered symbols to AlphaAPIHandler.")

        filteredSymbols = self.RetrieveListOfFilteredSymbols(
            ERepositoryAction.EARNINGS)

        apiagent = AlphaAPIHandler()

        apiagent.GetEarningsDateFromJsonAPIAndWriteToJSONFileBatch(
            filteredSymbols)

    def RetrieveListOfFilteredSymbols(self, eRepositoryAction: ERepositoryAction):
        """Retrieves a list of filtered symbols based off what is already with the Json repository.

        Returns:
            list: Filtered list of symbols.
        """

        symbolListGenerator = SymbolListGenerator(self.__filename)

        symbolListGenerator.CreateListOfSymbolsFromDataFrame(self.__columnname)

        filteredSymbolList = symbolListGenerator.CreateFilteredListOfSymbols(
            eRepositoryAction)

        Logger.LogInfo(
            f"Creating a filtered list of symbols. Count {len(filteredSymbolList)}")
        return filteredSymbolList

    def ProcessFilesJsonPriceFiles(self):
        sqlio = SQLIO()
        sqlio.InsertPriceDataFromJsonBatch()
        print("Finished processing files in folder.")
