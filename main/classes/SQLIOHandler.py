from main.enums.EJsonFolder import EJsonFolder
from main.classes.SQLIO import SQLIO


class SQLIOHandler():
    def __init__(self) -> None:
        self.__sqlIo__ = SQLIO()

    def ProcessFilesJsonPriceFiles(self):
        self.__sqlIo__.InsertPriceDataFromJsonBatch(EJsonFolder.PRICES)
        print(
            f"Finished processing files in {EJsonFolder.PRICES.value} folder.")
