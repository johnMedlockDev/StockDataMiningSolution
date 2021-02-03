from classes.HistoricSymbolDataGenerator import HistoricSymbolDataGenerator
from os import sys


if __name__ == "__main__":
    historicSymbolDataGenerator = HistoricSymbolDataGenerator('symbols.csv')
    historicSymbolDataGenerator.GenerateJsonSymbolRepository()
    sys.exit(0)
