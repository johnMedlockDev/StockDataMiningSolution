
from main.classes.SymbolListGenerator import SymbolListGenerator
from main.classes.SQLIOHandler import SQLIOHandler
from main.enums.EJsonFolder import EJsonFolder
from main.classes.AlphaAPIHTTPHandler import AlphaAPIHTTPHandler

from os import sys


if __name__ == "__main__":
    alphaAPIHTTPHandler = AlphaAPIHTTPHandler("redo", "SYMBOL")
    alphaAPIHTTPHandler.GenerateJsonSymbolPriceRepository()

    # symbolListGenerator = SymbolListGenerator("symbols", "SYMBOL")
    # symbolListGenerator.CreateFilteredListOfSymbols(
    #     [EJsonFolder.PRICES, EJsonFolder.REDO])

    sys.exit(0)
