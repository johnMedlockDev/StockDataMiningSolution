from main.enums.EJsonFolder import EJsonFolder
import os
from typing import List
from main.enums.EPayload import EPayload
from main.classes.Logger import Logger
from main.classes.JsonIO import JsonIO
import requests
from time import sleep, time
from dotenv import load_dotenv


class AlphaAPIHandler():
    """Handles www.alphavantage.co API actions.

    """

    def __init__(self) -> None:
        super().__init__()
        load_dotenv('io\env\secret.env')
        self.BASEURL = r'https://www.alphavantage.co/query?'
        self.APIKEY = f'{os.environ.get("api-token")}'
        self.__logger = Logger()

    def GetHistoricalPriceDataFromJsonAPI(self, symbol: str, payload: EPayload):
        """Makes a GET Request to AlphaVantage.

        Args:
            symbol (str): "IBM"
            payload (EPayload):  EPayload.FULL || EPayload.COMPACT

        Returns:
            jsonResponse (dict): JSON dictionary of historic symbol data.
        """

        SYMBOL = symbol.upper()
        SIZE = payload.value
        ROUTE = f'function=TIME_SERIES_DAILY&symbol={SYMBOL}&outputsize={SIZE}&apikey={self.APIKEY}'
        URI = self.BASEURL + ROUTE

        self.__response = requests.get(URI)

        try:
            if self.__response.status_code == 200:
                self.__logger.LogInfo(f" {SYMBOL} : Success!")
                return self.__response.json()['Time Series (Daily)']
            else:
                self.__logger.LogError(f"Server error!")
        except KeyError:
            try:
                self.__logger.LogInfo(
                    f" {SYMBOL} : {self.__response.json()['Error Message']}")
                return self.__response.json()['Error Message']
            except:
                self.__logger.LogInfo(
                    f" {SYMBOL} : {self.__response.json()['Information']}")
                return self.__response.json()['Information']

    def GetHistoricalPriceDataFromJsonAPIAndWriteToJSONFileBatch(self, symbolList: List, payload: EPayload):
        """Makes a GET Request to AlphaVantage for every symbol in a list.

        Args:
            symbolList (List): ['AAA','BBB']
            payload (EPayload): EPayload.FULL || EPayload.COMPACT

        """

        timeout = 15
        counter = 0
        jsonIo = JsonIO()

        jsonResponse = ""
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
                    self.__logger.LogInfo(f" {jsonResponse}")
                    break

                if counter >= 500:
                    self.__logger.LogError(
                        f"You reached the daily request limit, but you were able to make {counter} requests!")
                    break
                else:
                    self.__logger.LogError(
                        f" The timeout of {timeout} is too short!")
                    break

    def GetEarningsDateFromJsonAPI(self, symbol: str, timePeriod: str):
        """Makes a request to the Alpha API to get all the earnings date data.

        Args:
            symbol (str): "IBM"
            timePeriod (str): [description]

        Returns:
            jsonResponse (dict): JSON dictionary of historic symbol data.
        """
        if timePeriod == "quarterly":
            SYMBOL = symbol.upper()
            ROUTE = f'function=EARNINGS&symbol={SYMBOL}&apikey={self.APIKEY}'
            URI = self.BASEURL + ROUTE

            self.__response = requests.get(URI)
            try:
                if self.__response.status_code == 200:
                    self.__logger.LogInfo(f" {SYMBOL} : Success!")

                    return self.__response.json()['quarterlyEarnings']
                else:
                    self.__logger.LogError(f"Server error!")
            except KeyError:
                try:
                    self.__logger.LogInfo(
                        f" {SYMBOL} : {self.__response.json()['Error Message']}")
                    return self.__response.json()['Error Message']
                except:
                    self.__logger.LogInfo(
                        f" {SYMBOL} : {self.__response.json()['Information']}")
                    return self.__response.json()['Information']
        else:
            return self.__response.json()['annualEarnings']

    def GetEarningsDateFromJsonAPIAndWriteToJSONFileBatch(self, symbolList: List):
        """Makes a GET Request to AlphaVantage for every symbol in a list.

        Args:
            symbolList (List): ['AAA','BBB']
        """

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
                    self.__logger.LogInfo(f" {jsonResponse}")
                    break
                if r"{ }" in jsonResponse:
                    self.__logger.LogInfo(f" {jsonResponse}")
                    break

                if counter >= 500:
                    self.__logger.LogError(
                        f"You reached the daily request limit, but you were able to make {counter} requests!")
                    break
                else:
                    self.__logger.LogError(
                        f" The timeout of {timeout} is too short!")
                    break
