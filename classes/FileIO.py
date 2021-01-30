import pandas 

class FileIO(object):
    """Reads data from CSV documents and provides a list"""
    def  __init__(self,filename):
        self.__FILENAME = filename
        self.__DFList = []
        self.DF = pandas.read_csv(self.__FILENAME)  
        
    def CreateInMemoryListFromDataFrame(self, columnname):
        self.__DFList = self.DF[columnname].to_list()
        
    def GetInMemoryListFromDataFrame(self):
        return self.__DFList
