
from main.enums.EJsonFolder import EJsonFolder
from main.classes.AlphaAPIHTTPHandler import AlphaAPIHTTPHandler

from os import sys


if __name__ == "__main__":
    alphaAPIHTTPHandler = AlphaAPIHTTPHandler("symbols", "SYMBOL")
    alphaAPIHTTPHandler.GenerateJsonSymbolPriceRepository(
        [EJsonFolder.PRICES, EJsonFolder.REDO])
    sys.exit(0)
