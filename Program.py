from classes.enums.EPayload import EPayload
from os import sys
from classes.AlphaAPIHandler import AlphaAPIHandler
from classes.SymbolListGenerator import SymbolListGenerator


if __name__ == "__main__":
    FILENAME = r'symbols.csv'

    symbolListGenerator = SymbolListGenerator(FILENAME)

    symbolListGenerator.CreateListOfSymbolsFromDataFrame('SYMBOL')

    filteredSymbolList = symbolListGenerator.CreateFilteredListOfSymbols()

    apiagent = AlphaAPIHandler()

    apiagent.GetHistoricalPriceDataFromJsonAPIAndWriteToJSONFileBatch(
        filteredSymbolList, EPayload.FULL)

    sys.exit(0)
