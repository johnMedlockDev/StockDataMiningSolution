from main.enums.EJsonFolder import EJsonFolder
from main.classes.SQLIO import SQLIO
from main.enums.EPayload import EPayload
from os import sys
from main.classes.AlphaAPIHandler import AlphaAPIHandler
from main.classes.SymbolListGenerator import SymbolListGenerator
from main.classes.Logger import Logger


class HistoricDataHandler():

    def __init__(self, filename: str, columnname: str) -> None:
        super().__init__()
        self.__symbolListGenerator__ = SymbolListGenerator(
            filename, columnname)

    def GenerateJsonSymbolPriceRepository(self, eJsonFolders: list(EJsonFolder), payload: EPayload = EPayload.FULL):

        Logger.LogInfo("Passing filtered symbols to AlphaAPIHandler.")

        filteredSymbols = self.__symbolListGenerator__.CreateFilteredListOfSymbols(
            eJsonFolders)

        apiagent = AlphaAPIHandler()

        apiagent.GetHistoricalPriceDataFromJsonAPIAndWriteToJSONFileBatch(
            filteredSymbols, payload)

    def GenerateJsonSymbolEarningsRepository(self, eJsonFolders: list(EJsonFolder)):

        Logger.LogInfo("Passing filtered symbols to AlphaAPIHandler.")

        filteredSymbols = self.__symbolListGenerator__.CreateFilteredListOfSymbols(
            eJsonFolders)

        apiagent = AlphaAPIHandler()

        apiagent.GetEarningsDateFromJsonAPIAndWriteToJSONFileBatch(
            filteredSymbols)
