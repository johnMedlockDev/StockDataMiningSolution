import json
from main.classes.JsonIO import JsonIO
from main.classes.HistoricSymbolDataGenerator import HistoricSymbolDataGenerator
from main.classes.SQLIO import SQLIO
from os import sys


if __name__ == "__main__":
    # historicSymbolDataGenerator = HistoricSymbolDataGenerator('symbols.csv')
    # historicSymbolDataGenerator.GenerateJsonSymbolEarningsRepository()

    sqlio = SQLIO()
    for x in range(20):
        try: 
            sqlio.InsertPriceDataFromJsonBatch()
        except RecursionError:
            sqlio.InsertPriceDataFromJsonBatch()

    sys.exit(0)
