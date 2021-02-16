

from main.enums.EJsonFolder import EJsonFolder
from main.classes.SQLIO import SQLIO


class SQLIOHandler():
    def __init__(self) -> None:
        self.__sqlIo__ = SQLIO()

    def ProcessFilesJsonPriceFiles(self):
        eJsonFolder = EJsonFolder.PRICES
        self.__sqlIo__.InsertPriceDataFromJsonBatch(eJsonFolder)
        print("Finished processing files in folder.")
