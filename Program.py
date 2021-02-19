from main.classes.SQLIOHandler import SQLIOHandler
from main.classes.AlphaAPIHTTPHandler import AlphaAPIHTTPHandler

from os import sys
sys.setrecursionlimit(500000)

if __name__ == "__main__":

    alphaAPIHTTPHandler = AlphaAPIHTTPHandler("symbols", "SYMBOL")
    alphaAPIHTTPHandler.GenerateJsonSymbolOverviewRepository()

    # sQLIOHandler = SQLIOHandler()
    # sQLIOHandler.ProcessFilesJsonPriceFiles()

    sys.exit(0)
