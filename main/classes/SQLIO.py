import json
from main.enums.EJsonFolder import EJsonFolder
import pathlib
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
            jsonData = {}
            Logger.LogInfo(
                "Json Price Batch Job is Finished, because there was no file to be retrieved from the folder.")
        preparedJsonArray = []
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
                oldJsonFilePath = f"{pathlib.Path().absolute()}\\io\\json\\prices\\done\\{symbol}.json"
                newJsonFilePath = f"{pathlib.Path().absolute()}\\io\\json\\prices\\redo\\{symbol}.json"
                os.replace(oldJsonFilePath, newJsonFilePath)
                Logger.LogError(f"Needs to be pulled again {symbol}.")
                break
        self.InsertPriceDataFromJsonMany(preparedJsonArray)
        if jsonData != {}:
            self.InsertPriceDataFromJsonBatch(eJsonFolder)

    def InsertPriceDataFromJsonMany(self, preparedJsonArray: list):

        table = "HistoricPriceData"

        sql = f"""INSERT INTO {table} (Symbol, Date, OpenPrice, HighPrice, LowPrice,ClosePrice,Volume) VALUES (?,?,?,?,?,?,?)"""
        try:
            self.__cursor__.executemany(sql, preparedJsonArray)

            self.__connection__.commit()

            Logger.LogInfo(
                f"Inserted {preparedJsonArray} into {table}")
        except:
            Logger.LogError(
                f"failed to insert {preparedJsonArray} into {table}")
