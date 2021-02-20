

from main.classes.SQLIOHandler import SQLIOHandler
from os import sys

if __name__ == "__main__":

    # alphaAPIHTTPHandler = AlphaAPIHTTPHandler("symbols", "SYMBOL")
    # alphaAPIHTTPHandler.GenerateJsonSymbolOverviewRepository()

    sQLIOHandler = SQLIOHandler()
    sQLIOHandler.ProcessAllJsonFilesIntoDatabase()

    sys.exit(0)
