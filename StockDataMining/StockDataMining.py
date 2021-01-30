from classes.FileIO import FileIO

if __name__ == "__main__":

    FILENAME = r'C:\Users\John\source\repos\StockDataMiningSolution\StockDataMining\files\csvs\source\tickers-scrubbed.csv'

    file = FileIO(FILENAME)

    file.CreateInMemoryListFromDataFrame('SYMBOL')
    result = file.GetInMemoryListFromDataFrame()
    print(result)
