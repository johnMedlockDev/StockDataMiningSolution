from main.classes.PathHelper import PathHelper
from main.enums.EJsonFolder import EJsonFolder
from main.classes.Logger import Logger
from main.classes.JsonIO import JsonIO
import pyodbc
from dotenv import load_dotenv
import os


class SQLIO:
    def __init__(self) -> None:
        load_dotenv('io\env\secret.env')
        self.__connection__ = pyodbc.connect(
            os.environ.get("connectionString"))
        self.__cursor__ = self.__connection__.cursor()
        self.__jsonIo__ = JsonIO()

    def InsertPriceDataFromJsonBatch(self, eJsonFolder: EJsonFolder):

        jsonDataArray = self.__jsonIo__.ReadJsonFromFile(eJsonFolder)

        try:
            symbol = jsonDataArray[0]
            jsonData = jsonDataArray[1]
        except IndexError:
            symbol = ''
            jsonData = {"done": "done"}
            Logger.LogInfo(
                "Json Price Batch Job is Finished, because there was no file to be retrieved from the folder.")

        preparedJsonArray = []

        if symbol != '':
            for key in jsonData:
                try:
                    Symbol = symbol
                    Date = key
                    OpenPrice = jsonData[key]["1. open"]
                    HighPrice = jsonData[key]["2. high"]
                    LowPrice = jsonData[key]["3. low"]
                    ClosePrice = jsonData[key]["4. close"]
                    Volume = jsonData[key]["5. volume"]
                    preparedJsonArray.append(
                        (Symbol, Date, OpenPrice, HighPrice, LowPrice, ClosePrice, Volume))
                except TypeError:
                    self.SwapFiles(eJsonFolder, symbol)
                    Logger.LogError(f"Needs to be pulled again {symbol}.")
                    break
            self.InsertPriceDataFromJsonMany(preparedJsonArray)

        if jsonData != {"done": "done"}:
            self.InsertPriceDataFromJsonBatch(eJsonFolder)

    def InsertPriceDataFromJsonMany(self, preparedJsonArray: list):

        table = "HistoricPriceData"

        sql = f"""INSERT INTO {table} (Symbol, Date, OpenPrice, HighPrice, LowPrice,ClosePrice,Volume) VALUES (?,?,?,?,?,?,?)"""

        self.ExecuteSql(sql, table, preparedJsonArray)

    def ExecuteSql(self, sql: str, table: str, preparedJsonArray: list):
        try:
            self.__cursor__.executemany(sql, preparedJsonArray)

            self.__connection__.commit()

            Logger.LogInfo(
                f"Inserted {preparedJsonArray} into {table}")
        except:
            Logger.LogError(
                f"failed to insert {preparedJsonArray} into {table}")

    def SwapFiles(self, eJsonFolder: EJsonFolder, symbol: str):
        oldJsonFilePath = f"{PathHelper.JsonRoot()}\\{eJsonFolder.value}\\done\\{symbol}.json"
        newJsonFilePath = f"{PathHelper.JsonRoot()}\\{eJsonFolder.value}\\redo\\{symbol}.json"
        os.replace(oldJsonFilePath, newJsonFilePath)

