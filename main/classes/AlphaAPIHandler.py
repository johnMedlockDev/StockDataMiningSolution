import os
from typing import List
from main.enums.EPayload import EPayload
from main.classes.Logger import Logger
from main.classes.JsonIO import JsonIO
import requests
from time import sleep
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
            dict: JSON dictionary of historic symbol data.
        """

        SYMBOL = symbol.upper()
        SIZE = payload.value
        ROUTE = f'function=TIME_SERIES_DAILY&symbol={SYMBOL}&outputsize={SIZE}&apikey={self.APIKEY}'
        URI = self.BASEURL + ROUTE

        response = requests.get(URI)

        try:
            if response.status_code == 200:
                self.__logger.LogInfo(
                    f" {SYMBOL} : Success!")
                return response.json()['Time Series (Daily)']
            else:
                self.__logger.LogError(f"Server error!")
        except KeyError:
            try:
                self.__logger.LogInfo(
                    f" {SYMBOL} : {response.json()['Error Message']}")
                return response.json()['Error Message']
            except KeyError:
                self.__logger.LogInfo(
                    f" {SYMBOL} : {response.json()['Information']}")
                return response.json()['Information']

    def GetHistoricalPriceDataFromJsonAPIAndWriteToJSONFileBatch(self, symbolList: List, payload: EPayload):
        """Makes a GET Request to AlphaVantage for every symbol in a list.

        Args:
            symbolList (List): ['AAA','BBB']
            payload (EPayload): EPayload.FULL || EPayload.COMPACT
        """

        timeout = 15
        counter = 0

        jsonIo = JsonIO()

        for symbol in symbolList:
            try:
                jsonIo.WriteJsonToFile(
                    symbol, self.GetHistoricalPriceDataFromJsonAPI(symbol, payload))
                sleep(timeout)
                counter += 1
            except KeyError:
                if counter >= 500:
                    self.__logger.LogError(
                        f"You reached the daily request limit, but you were able to make {counter} requests!")
                else:
                    self.__logger.LogError(
                        f" The timeout of {timeout} is too short!")
                break
