from typing import List
from classes.enums.EPayload import EPayload
from classes.Logger import Logger
from classes.JsonIO import JsonIO
import requests
from time import sleep


class AlphaAPIHandler(object):
    '''
    Handles www.alphavantage.co API actions.

    '''

    def __init__(self) -> None:
        super().__init__()
        self.BASEURL = r'https://www.alphavantage.co/query?'
        self.APIKEY = r'0ZZU6DYNDO3BUCVR'
        self.logger = Logger()

    def GetHistoricalPriceDataFromJsonAPI(self, symbol: str, payload: EPayload):
        '''
        Makes a GET Request to AlphaVantage.

        :parma: symbol = "ibm"

        :parma: payload = EPayload.FULL || EPayload.COMPACT

        '''

        SYMBOL = symbol.upper()
        SIZE = payload  # full | compact
        ROUTE = f'function=TIME_SERIES_DAILY&symbol={SYMBOL}&outputsize={SIZE}&apikey={self.APIKEY}'

        URI = self.BASEURL + ROUTE

        response = requests.get(URI)

        try:
            if response.status_code == 200:
                self.logger.LogInfo(
                    f" {SYMBOL} : Success!")
                return response.json()['Time Series (Daily)']
            else:
                self.logger.LogError(
                    f"Server error!")

        except KeyError:
            self.logger.LogInfo(
                f" {SYMBOL} : {response.json()['Error Message']}")
            return response.json()['Error Message']

    def GetHistoricalPriceDataFromJsonAPIAndWriteToJSONFileBatch(self, symbolList: List, payload: EPayload):
        ''' 
        Makes a GET Request to AlphaVantage for every symbol in a list.

        :parma: symbolList = ['AAA','BBB']

        :parma: payload = EPayload.FULL || EPayload.COMPACT

        '''
        timeout = 15

        SIZE = payload
        jsonIo = JsonIO()

        for symbol in symbolList:
            SYMBOL = symbol.upper()
            # full | compact
            ROUTE = f'function=TIME_SERIES_DAILY&symbol={SYMBOL}&outputsize={SIZE}&apikey={self.APIKEY}'

            URI = self.BASEURL + ROUTE
            response = requests.get(URI)

            try:
                if response.status_code == 200:
                    self.logger.LogInfo(
                        f"{SYMBOL} : JSON GET Request was a Success!")
                    jsonIo.WriteJsonToFile(SYMBOL, response.json()[
                                           'Time Series (Daily)'])
                    sleep(12)
                else:
                    self.logger.LogError(f"Server error!")
            except KeyError:
                try:
                    self.logger.LogError(
                        f" {SYMBOL} : {response.json()['Error Message']}")
                except KeyError:
                    self.logger.LogError(
                        f" The timeout of {timeout} is too short : {response.json()['Information']}")
                    break
