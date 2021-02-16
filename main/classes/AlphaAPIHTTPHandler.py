from main.enums.EJsonFolder import EJsonFolder
from main.classes.SQLIO import SQLIO
from main.enums.EPayload import EPayload
from os import sys
from main.classes.AlphaAPIHTTP import AlphaAPIHTTP
from main.classes.SymbolListGenerator import SymbolListGenerator
from main.classes.Logger import Logger


class AlphaAPIHTTPHandler():

    def __init__(self, filename: str, columnname: str) -> None:
        self.__symbolListGenerator__ = SymbolListGenerator(
            filename, columnname)
        self.__apiagent___ = AlphaAPIHTTP()

    def GenerateJsonSymbolPriceRepository(self, eJsonFolders: list(EJsonFolder), payload: EPayload = EPayload.FULL):

        Logger.LogInfo("Passing filtered symbols to AlphaAPIHTTP.")

        filteredSymbols = self.__symbolListGenerator__.CreateFilteredListOfSymbols(
            eJsonFolders)

        self.__apiagent___.GetHistoricalPriceDataFromJsonAPIAndWriteToJSONFileBatch(
            filteredSymbols, payload)

    def GenerateJsonSymbolEarningsRepository(self, eJsonFolders: list(EJsonFolder)):

        Logger.LogInfo("Passing filtered symbols to AlphaAPIHTTP.")

        filteredSymbols = self.__symbolListGenerator__.CreateFilteredListOfSymbols(
            eJsonFolders)

        self.__apiagent___.GetEarningsDateFromJsonAPIAndWriteToJSONFileBatch(
            filteredSymbols)
