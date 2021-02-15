import json
import pathlib
from main.classes.Logger import Logger
import symbol
from main.classes.JsonIO import JsonIO
import pyodbc
from dotenv import load_dotenv
import os


class SQLIO:
    def __init__(self) -> None:
        load_dotenv('io\env\secret.env')
        self.server = f'{os.environ.get("server")}'
        self.database = f'{os.environ.get("database")}'
        self.connection = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};' +
                                         f'SERVER={self.server};DATABASE={self.database};Trusted_Connection=yes;')
        self.cursor = self.connection.cursor()
        self.jsonIo = JsonIO()
        self.__logger = Logger()

    def InsertPriceDataFromJson(self, Symbol: str, Date: str, OpenPrice: str, HighPrice: str, LowPrice: str, ClosePrice: str, Volume: str):
        """Inserts a price data record into a table
            Args:
                Symbol (str) : The symbol of the company.
                Date (str) :  The date time.
                OpenPrice (str) : The Open price.
                HighPrice (str) : The High price.
                LowPrice (str) : The Low price.
                ClosePrice (str) : The Closing price.
                Volume (str) : The volume for the day.
        """
        table = "HistoricPriceData"

        sql = f"""INSERT INTO {table} (Symbol, Date, OpenPrice, HighPrice, LowPrice,ClosePrice,Volume) VALUES (?,?,?,?,?,?,?)"""
        try:
            self.cursor.execute(sql, Symbol, Date, OpenPrice,
                                HighPrice, LowPrice, ClosePrice, Volume)

            self.connection.commit()

            self.__logger.LogInfo(
                f"Inserted {Symbol}, {Date}, {OpenPrice}, {HighPrice}, {LowPrice}, {ClosePrice}, {Volume} into {table}")
        except:
            self.__logger.LogError(
                f"failed to insert {Symbol} {Date} into {table}")

    def InsertPriceDataFromJsonBatch(self):
        ''' Recursive solution to get json data from a folder and insert it into a database.

        '''
        jsonDataArray = self.jsonIo.RetrieveJsonFromFile("prices")
        symbol = jsonDataArray[0]
        jsonData = jsonDataArray[1]

        for key in jsonData:
            try:
                Symbol = symbol
                Date = key
                OpenPrice = jsonData[key]["1. open"]
                HighPrice = jsonData[key]["2. high"]
                LowPrice = jsonData[key]["3. low"]
                ClosePrice = jsonData[key]["4. close"]
                Volume = jsonData[key]["5. volume"]
                self.InsertPriceDataFromJson(
                    Symbol, Date, OpenPrice, HighPrice, LowPrice, ClosePrice, Volume)
            except TypeError:
                oldJsonFilePath = f"{pathlib.Path().absolute()}\\io\\json\\prices\\done\\{symbol}.json"
                newJsonFilePath = f"{pathlib.Path().absolute()}\\io\\json\\prices\\redo\\{symbol}.json"
                os.replace(oldJsonFilePath, newJsonFilePath)
                self.__logger.LogError(f"Needs to be pulled again {symbol}.")
                break

        self.InsertPriceDataFromJsonBatch()
