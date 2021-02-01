from json import dump
import pathlib
from classes.Logger import Logger


class JsonIO(object):
    '''
    Write Json to file based of symbol name.

    '''

    def __init__(self) -> None:
        super().__init__()
        self.logger = Logger()

    def WriteJsonToFile(self, symbol: str, jsonObject: dict):
        '''
        Writes Json to file based of symbol name.

        :parma: symbol = 'ibm'

        :parma: jsonObject = {"2021-01-29": {"1. open": "25.1600", "2. high": "25.1600", "3. low": "25.1450", "4. close": "25.1450", "5. volume": "3099"}

        '''
        try:
            with open(f'{pathlib.Path().absolute()}\\io\\json\\{symbol.upper()}.json', 'w') as outfile:
                dump(jsonObject, outfile)
                self.logger.LogInfo(
                    f"Successful JSON file creation of {symbol}!")
        except:
            self.logger.LogError(f"Failure JSON file creation of {symbol}!")
