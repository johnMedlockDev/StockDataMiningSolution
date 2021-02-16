from main.enums.EJsonFolder import EJsonFolder
import os
from typing import List
from main.enums.EPayload import EPayload
from main.classes.Logger import Logger
from main.classes.JsonIO import JsonIO
import requests
from time import sleep
from dotenv import load_dotenv


class AlphaAPIHandler():

    def __init__(self) -> None:
        super().__init__()
        load_dotenv('io\env\secret.env')
        self.__BASEURL__ = r'https://www.alphavantage.co/query?'
        self.__APIKEY__ = f'{os.environ.get("api-token")}'

    def GetHistoricalPriceDataFromJsonAPI(self, symbol: str, payload: EPayload):

        SYMBOL = symbol.upper()
        SIZE = payload.value
        ROUTE = f'function=TIME_SERIES_DAILY&symbol={SYMBOL}&outputsize={SIZE}&apikey={self.__APIKEY__}'
        URI = self.__BASEURL__ + ROUTE

        self.__response = requests.get(URI)

        try:
            if self.__response.status_code == 200:
                Logger.LogInfo(f" {SYMBOL} : Success!")
                return self.__response.json()['Time Series (Daily)']
            else:
                Logger.LogError(f"Server error!")
        except KeyError:
            try:
                Logger.LogInfo(
                    f" {SYMBOL} : {self.__response.json()['Error Message']}")
                return self.__response.json()['Error Message']
            except:
                Logger.LogInfo(
                    f" {SYMBOL} : {self.__response.json()['Information']}")
                return self.__response.json()['Information']

    def GetHistoricalPriceDataFromJsonAPIAndWriteToJSONFileBatch(self, symbolList: List, payload: EPayload):

        timeout = 15
        counter = 0
        jsonIo = JsonIO()

        jsonResponse = []
        for symbol in symbolList:
            try:
                try:
                    jsonResponse = self.GetHistoricalPriceDataFromJsonAPI(
                        symbol, payload)
                    jsonIo.WriteJsonToFile(
                        symbol, EJsonFolder.PRICES, jsonResponse)
                    sleep(timeout)
                    counter += 1
                except:
                    continue
            except KeyError:
                if r"https://www.alphavantage.co/premium/" in jsonResponse:
                    Logger.LogInfo(f" {jsonResponse}")
                    break

                if counter >= 500:
                    Logger.LogError(
                        f"You reached the daily request limit, but you were able to make {counter} requests!")
                    break
                else:
                    Logger.LogError(
                        f" The timeout of {timeout} is too short!")
                    break

    def GetEarningsDateFromJsonAPI(self, symbol: str, timePeriod: str):

        if timePeriod == "quarterly":
            SYMBOL = symbol.upper()
            ROUTE = f'function=EARNINGS&symbol={SYMBOL}&apikey={self.__APIKEY__}'
            URI = self.__BASEURL__ + ROUTE

            self.__response = requests.get(URI)
            try:
                if self.__response.status_code == 200:
                    Logger.LogInfo(f" {SYMBOL} : Success!")

                    return self.__response.json()['quarterlyEarnings']
                else:
                    Logger.LogError(f"Server error!")
            except KeyError:
                try:
                    Logger.LogInfo(
                        f" {SYMBOL} : {self.__response.json()['Error Message']}")
                    return self.__response.json()['Error Message']
                except:
                    Logger.LogInfo(
                        f" {SYMBOL} : {self.__response.json()['Information']}")
                    return self.__response.json()['Information']
        else:
            return self.__response.json()['annualEarnings']

    def GetEarningsDateFromJsonAPIAndWriteToJSONFileBatch(self, symbolList: List):

        timeout = 15
        counter = 0
        jsonIo = JsonIO()

        jsonResponse = []
        for symbol in symbolList:
            try:
                try:
                    jsonResponse = self.GetEarningsDateFromJsonAPI(
                        symbol, "quarterly")

                    jsonIo.WriteJsonToFile(
                        symbol, EJsonFolder.QUARTERLY, jsonResponse)

                    jsonResponse = self.GetEarningsDateFromJsonAPI(
                        symbol, "annual")

                    jsonIo.WriteJsonToFile(
                        symbol, EJsonFolder.ANNUAL, jsonResponse)

                    print(jsonResponse)
                    sleep(timeout)
                    counter += 1
                except:
                    continue
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
                else:
                    Logger.LogError(
                        f" The timeout of {timeout} is too short!")
                    break
