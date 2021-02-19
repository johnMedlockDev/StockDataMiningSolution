from main.enums.EJsonFolder import EJsonFolder
from main.enums.EPayload import EPayload
from main.classes.AlphaAPIHTTP import AlphaAPIHTTP
from main.classes.SymbolListGenerator import SymbolListGenerator
from main.classes.Logger import Logger


class AlphaAPIHTTPHandler():

    def __init__(self, filename: str, columnname: str) -> None:
        self.__symbolListGenerator__ = SymbolListGenerator(
            filename, columnname)
        self.__apiagent___ = AlphaAPIHTTP()

    def GenerateJsonSymbolPriceRepository(self, eJsonFolder: EJsonFolder = EJsonFolder.NONE, payload: EPayload = EPayload.FULL):

        Logger.LogInfo("Generating filtered symbols.")
        filteredSymbols = self.__symbolListGenerator__.CreateFilteredListOfSymbols(
            [EJsonFolder.PRICES, eJsonFolder])

        Logger.LogInfo("Passing filtered symbols to AlphaAPIHTTP.")

        self.__apiagent___.GetHistoricalPriceDataFromJsonAPIAndWriteToJSONFileBatch(
            filteredSymbols, payload)

        Logger.LogInfo("Finished getting filter list from AlphaAPIHTTP.")

    def GenerateJsonSymbolEarningsRepositories(self, eJsonFolder: EJsonFolder = EJsonFolder.NONE):

        Logger.LogInfo("Generating filtered symbols.")
        filteredSymbols = self.__symbolListGenerator__.CreateFilteredListOfSymbols(
            [EJsonFolder.QUARTERLYBALANCE, eJsonFolder])

        Logger.LogInfo("Passing filtered symbols to AlphaAPIHTTP.")
        self.__apiagent___.GetEarningsDataFromJsonAPIAndWriteToJSONFileBatch(
            filteredSymbols)

        Logger.LogInfo("Finished getting filter list from AlphaAPIHTTP.")

    def GenerateJsonSymbolOverviewRepository(self, eJsonFolder: EJsonFolder = EJsonFolder.NONE):

        Logger.LogInfo("Generating filtered symbols.")
        filteredSymbols = self.__symbolListGenerator__.CreateFilteredListOfSymbols(
            [EJsonFolder.OVERVIEW, eJsonFolder])

        Logger.LogInfo("Passing filtered symbols to AlphaAPIHTTP.")
        self.__apiagent___.GetCompanyOverviewFromJsonAPIAndWriteToJSONFileBatch(
            filteredSymbols)

        Logger.LogInfo("Finished getting filter list from AlphaAPIHTTP.")
