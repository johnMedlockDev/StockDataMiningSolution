from classes.enums.EPayload import EPayload
from os import sys
from classes.AlphaAPIHandler import AlphaAPIHandler
from classes.SymbolListGenerator import SymbolListGenerator


if __name__ == "__main__":
    FILENAME = r'symbols.csv'

    symbolListGenerator = SymbolListGenerator(FILENAME)

    symbolListGenerator.CreateListFromDataFrame('SYMBOL')

    symbolList = symbolListGenerator.GetListFromDataFrame()

    apiagent = AlphaAPIHandler()

    apiagent.GetHistoricalPriceDataFromJsonAPIAndWriteToJSONFileBatch(
        symbolList, EPayload.FULL)

    sys.exit(0)
