from main.enums.EJsonFolder import EJsonFolder
from main.classes.SQLIO import SQLIO


class SQLIOHandler():

    def ProcessAllJsonFilesIntoDatabase(self):

        folders = [EJsonFolder.ANNUALBALANCE, EJsonFolder.ANNUALCASH, EJsonFolder.ANNUALINCOME, EJsonFolder.QUARTERLYBALANCE,
                   EJsonFolder.QUARTERLYCASH, EJsonFolder.QUARTERLYINCOME, EJsonFolder.PRICES, EJsonFolder.OVERVIEW]

        for folder in folders:
            self.__sqlIo__ = SQLIO(folder)
            print(f"Starting to process files in {folder.value} folder.")
            self.__sqlIo__.InsertDataFromJsonBatch()
            print(f"Finished processing files in {folder.value} folder.")
