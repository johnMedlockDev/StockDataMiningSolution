
from main.classes.SQLIOHandler import SQLIOHandler
from main.classes.SQLIO import SQLIO
from main.enums.EJsonFolder import EJsonFolder
from main.classes.SymbolListGenerator import SymbolListGenerator

from os import sys


if __name__ == "__main__":
    sqlHandler = SQLIOHandler()
    sqlHandler.ProcessFilesJsonPriceFiles()
    sys.exit(0)
