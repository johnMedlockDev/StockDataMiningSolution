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
        self.__timeout__ = 15

    def GetHistoricalPriceDataFromJsonAPIAndWriteToJSONFileBatch(self, symbolList: List, payload: EPayload):

        counter = 0

        jsonResponse = []
        for symbol in symbolList:
            try:
                try:
                    jsonResponse = self.GetHistoricalPriceDataFromJsonAPI(
                        symbol, payload)
                    self.__jsonIo__.WriteJsonToFile(
                        EJsonFolder.PRICES, symbol, jsonResponse)
                    sleep(self.__timeout__)
                    counter += 1
                except:
                    Logger.LogDebug(symbol)
                    break
            except KeyError:
                if r"https://www.alphavantage.co/premium/" in jsonResponse:
                    Logger.LogInfo(f" {jsonResponse}")
                    break

                if counter >= 500:
                    Logger.LogError(
                        f"You reached the daily request limit, but you were able to make {counter} requests!")
                    break
                Logger.LogError(
                    f" The timeout of {self.__timeout__} is too short!")
                break

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

    def GetEarningsDateFromJsonAPIAndWriteToJSONFileBatch(self, symbolList: List):

        counter = 0

        jsonResponse = []
        for symbol in symbolList:
            try:
                try:
                    jsonResponse = self.GetEarningsDateFromJsonAPI(
                        symbol, EJsonFolder.QUARTERLY)

                    self.__jsonIo__.WriteJsonToFile(
                        EJsonFolder.QUARTERLY, symbol, jsonResponse)

                    jsonResponse = self.GetEarningsDateFromJsonAPI(
                        symbol, EJsonFolder.ANNUAL)

                    self.__jsonIo__.WriteJsonToFile(
                        EJsonFolder.ANNUAL, symbol, jsonResponse)
                    sleep(self.__timeout__)
                    counter += 1
                except:
                    Logger.LogDebug(symbol)
                    break
            except KeyError:

                if r"https://www.alphavantage.co/premium/" in jsonResponse:
                    Logger.LogInfo(f" {jsonResponse}")
                    break
                if r"{ }" in jsonResponse:
                    Logger.LogInfo(f" {jsonResponse}")
                    break

                if counter >= 500:
                    Logger.LogError(
                        f"You reached the daily request limit, but you were able to make {counter} requests!")
                    break
                Logger.LogError(
                    f" The timeout of {self.__timeout__} is too short!")
                break

    def GetEarningsDateFromJsonAPI(self, symbol: str, eJsonFolder: EJsonFolder):

        if eJsonFolder == eJsonFolder.QUARTERLY:
            SYMBOL = symbol.upper()
            ROUTE = f'function=EARNINGS&symbol={SYMBOL}&apikey={self.__APIKEY__}'
            URI = self.__BASEURL__ + ROUTE

            self.__response__ = requests.get(URI)

            try:
                if self.__response__.status_code == 200:
                    Logger.LogInfo(f" {SYMBOL} : Success!")

                    return self.__response__.json()['quarterlyEarnings']
            except KeyError:
                try:
                    Logger.LogInfo(
                        f" {SYMBOL} : {self.__response__.json()['Error Message']}")

                    return self.__response__.json()['Error Message']
                except KeyError:
                    Logger.LogInfo(
                        f" {SYMBOL} : {self.__response__.json()['Information']}")

                    return self.__response__.json()['Information']
        return self.__response__.json()['annualEarnings']
