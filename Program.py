from main.classes.HistoricSymbolDataGenerator import HistoricSymbolDataGenerator
from os import sys


if __name__ == "__main__":
    historicSymbolDataGenerator = HistoricSymbolDataGenerator('symbols.csv')
    historicSymbolDataGenerator.GenerateJsonSymbolEarningsRepository()
    sys.exit(0)
