from classes.enums.EPayload import EPayload
from os import sys
from classes.AlphaAPIHandler import AlphaAPIHandler
from classes.SymbolListGenerator import SymbolListGenerator


if __name__ == "__main__":
    FILENAME = r'symbols.csv'

    fileAgent = SymbolListGenerator(FILENAME)

    fileAgent.CreateListFromDataFrame('SYMBOL')
    result = fileAgent.GetListFromDataFrame()

    apiagent = AlphaAPIHandler()
    responsejson = apiagent.GetHistoricalPriceDataFromJsonAPI(
        "ibm", EPayload.COMPACT)

    sys.exit(0)
