from classes.enums.EPayload import EPayload
from classes.Logger import Logger
import requests


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

        :parma: size = "full" || "compact"

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
