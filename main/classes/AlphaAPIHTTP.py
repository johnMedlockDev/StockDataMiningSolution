from main.enums.EJsonFolder import EJsonFolder
import os
from typing import List
from main.enums.EPayload import EPayload
from main.classes.Logger import Logger
from main.classes.JsonIO import JsonIO
import requests
from time import sleep
from dotenv import load_dotenv


class AlphaAPIHTTP():

    def __init__(self) -> None:
        load_dotenv('io\env\secret.env')
        self.__BASEURL__ = r'https://www.alphavantage.co/query?'
        self.__APIKEY__ = f'{os.environ.get("api-token")}'
        self.__jsonIo__ = JsonIO()
        self.__response__ = ''
        # self.__timeout__ = 15
        self.__timeout__ = .5

    def GetHistoricalPriceDataFromJsonAPIAndWriteToJSONFileBatch(self, symbolList: List, payload: EPayload):

        for symbol in symbolList:
            jsonResponse = self.GetHistoricalPriceDataFromJsonAPI(
                symbol, payload)

            if r"https://www.alphavantage.co/premium/" in jsonResponse:
                Logger.LogInfo(
                    f"You reached the daily request limit!")
                break

            self.__jsonIo__.WriteJsonToFile(
                EJsonFolder.PRICES, symbol, jsonResponse)
            sleep(self.__timeout__)

    def GetHistoricalPriceDataFromJsonAPI(self, symbol: str, payload: EPayload):

        SYMBOL = symbol.upper()
        SIZE = payload.value
        ROUTE = f'function=TIME_SERIES_DAILY&symbol={SYMBOL}&outputsize={SIZE}&apikey={self.__APIKEY__}'
        URI = self.__BASEURL__ + ROUTE

        self.__response__ = requests.get(URI)

        try:
            if self.__response__.status_code == 200:
                Logger.LogInfo(f" {SYMBOL} : Success!")
                return self.__response__.json()['Time Series (Daily)']
            Logger.LogError(f"Server error!")
        except KeyError:
            try:
                Logger.LogInfo(
                    f" {SYMBOL} : {self.__response__.json()['Error Message']}")
                return self.__response__.json()['Error Message']
            except:
                Logger.LogInfo(
                    f" {SYMBOL} : {self.__response__.json()['Information']}")
                return self.__response__.json()['Information']

    def GetEarningsDataFromJsonAPIAndWriteToJSONFileBatch(self, symbolList: List):
        reports = [EJsonFolder.ANNUALBALANCE, EJsonFolder.ANNUALCASH, EJsonFolder.ANNUALINCOME,
                   EJsonFolder.QUARTERLYBALANCE, EJsonFolder.QUARTERLYCASH,  EJsonFolder.QUARTERLYINCOME]

        for symbol in symbolList:
            for report in reports:

                jsonResponse = self.GetEarningsDataFromJsonAPI(
                    symbol, report)

                self.__jsonIo__.WriteJsonToFile(
                    report, symbol, jsonResponse)

    def GetEarningsDataFromJsonAPI(self, symbol: str, eJsonFolder: EJsonFolder):
        SYMBOL = symbol.upper()

        FUNCTION = ''
        print(symbol, eJsonFolder.value)
        if "balance" in eJsonFolder.value:
            FUNCTION = "BALANCE_SHEET"
        if "income" in eJsonFolder.value:
            FUNCTION = "CASH_FLOW"
        if "cash" in eJsonFolder.value:
            FUNCTION = "INCOME_STATEMENT"

        ROUTE = f'function={FUNCTION}&symbol={SYMBOL}&apikey={self.__APIKEY__}'
        print(ROUTE)
        URI = self.__BASEURL__ + ROUTE

        self.__response__ = requests.get(URI)

        print(self.__response__.json())
        if "quarterly" in eJsonFolder.value:
            try:
                return self.__response__.json()['quarterlyReports']
            except:
                return self.__response__.json()

        if "annual" in eJsonFolder.value:
            try:
                return self.__response__.json()['annualReports']
            except:
                return self.__response__.json()

    def GetCompanyOverviewFromJsonAPIAndWriteToJSONFileBatch(self, symbolList: List):
        for symbol in symbolList:
            jsonResponse = self.GetCompanyOverviewFromJsonAPI(
                symbol)

            self.__jsonIo__.WriteJsonToFile(
                EJsonFolder.OVERVIEW, symbol, jsonResponse)

    def GetCompanyOverviewFromJsonAPI(self, symbol: str):

        SYMBOL = symbol.upper()

        ROUTE = f'function=OVERVIEW&symbol={SYMBOL}&apikey={self.__APIKEY__}'

        URI = self.__BASEURL__ + ROUTE

        self.__response__ = requests.get(URI)

        print(self.__response__.json())
        return self.__response__.json()
