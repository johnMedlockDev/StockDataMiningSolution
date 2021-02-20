from main.classes.PathHelper import PathHelper
from main.enums.EJsonFolder import EJsonFolder
from main.classes.Logger import Logger
from main.classes.JsonIO import JsonIO
import pyodbc
from dotenv import load_dotenv
import os


class SQLIO:
    def __init__(self, eJsonFolder: EJsonFolder) -> None:
        load_dotenv('io\env\secret.env')
        self.__connection__ = pyodbc.connect(
            os.environ.get("connectionString"))
        self.__cursor__ = self.__connection__.cursor()
        self.__jsonIo__ = JsonIO()
        self.eJsonFolderContext = eJsonFolder

    def InsertDataFromJsonBatch(self):

        self.initalizedJsonList = self.InitializeJson()

        while(self.initalizedJsonList[1] != {"done": "done"}):

            preparedJsonList = []

            if self.initalizedJsonList[0] != '':
                preparedJsonList = self.PrepareJsonForSQL(
                    self.initalizedJsonList[1], self.initalizedJsonList[0], preparedJsonList)
                self.InsertDataFromJsonMany(preparedJsonList)

            self.initalizedJsonList = self.InitializeJson()

    def InitializeJson(self):
        jsonList = self.__jsonIo__.ReadJsonFromFile(
            self.eJsonFolderContext)
        try:
            symbol = jsonList[0]
            jsonData = jsonList[1]
        except IndexError:
            symbol = ''
            jsonData = {"done": "done"}
            Logger.LogInfo(
                "Json Price Batch Job is Finished, because there was no file to be retrieved from the folder.")

        return [symbol, jsonData]

    def PrepareJsonForSQL(self,  jsonData: dict, symbol: str, preparedJsonList: list):

        if self.eJsonFolderContext == EJsonFolder.OVERVIEW:

            try:
                Symbol = symbol
                Currency = jsonData['Currency']
                AssetType = jsonData['AssetType']
                Name = jsonData['Name']
                Description = jsonData['Description']
                Exchange = jsonData['Exchange']
                Country = jsonData['Country']
                Sector = jsonData['Sector']
                Industry = jsonData['Industry']
                preparedJsonList.extend(
                    [Symbol, Currency, AssetType, Name, Description, Exchange, Country, Sector, Industry])
            except TypeError:
                self.SwapFiles(symbol)
                Logger.LogError(
                    f"Needs to be pulled again {symbol}.")
            except KeyError:
                self.SwapFiles(symbol)
                Logger.LogError(
                    f"No info for {symbol}.")

            return [] if [tuple(preparedJsonList)] == [()] or [tuple(preparedJsonList)] == [[]] else [tuple(preparedJsonList)]

        if self.eJsonFolderContext == EJsonFolder.PRICES:

            for key in jsonData:
                try:
                    Symbol = symbol
                    Date = jsonData[key]
                    OpenPrice = jsonData[key]["1. open"]
                    HighPrice = jsonData[key]["2. high"]
                    LowPrice = jsonData[key]["3. low"]
                    ClosePrice = jsonData[key]["4. close"]
                    Volume = jsonData[key]["5. volume"]
                    preparedJsonList.append(
                        [Symbol, Date, OpenPrice, HighPrice, LowPrice, ClosePrice, Volume])
                except TypeError:
                    self.SwapFiles(symbol)
                    Logger.LogError(
                        f"Needs to be pulled again {symbol}.")
                    break

        if self.eJsonFolderContext == EJsonFolder.ANNUALINCOME or self.eJsonFolderContext == EJsonFolder.QUARTERLYINCOME:

            for key in jsonData:
                try:
                    Symbol = symbol
                    FilingType = "A" if "annual" in self.eJsonFolderContext.value else "Q"
                    FiscalDateEnding = key['fiscalDateEnding']
                    ReportedCurrency = key['reportedCurrency']
                    Investments = key['investments']
                    ChangeInLiabilities = key['changeInLiabilities']
                    CashflowFromInvestment = key['cashflowFromInvestment']
                    OtherCashflowFromInvestment = key['otherCashflowFromInvestment']
                    NetBorrowings = key['netBorrowings']
                    CashflowFromFinancing = key['cashflowFromFinancing']
                    OtherCashflowFromFinancing = key['otherCashflowFromFinancing']
                    ChangeInOperatingActivities = key['changeInOperatingActivities']
                    NetIncome = key['netIncome']
                    ChangeInCash = key['changeInCash']
                    OperatingCashflow = key['operatingCashflow']
                    OtherOperatingCashflow = key['otherOperatingCashflow']
                    Depreciation = key['depreciation']
                    DividendPayout = key['dividendPayout']
                    StockSaleAndPurchase = key['stockSaleAndPurchase']
                    ChangeInInventory = key['changeInInventory']
                    ChangeInAccountReceivables = key['changeInAccountReceivables']
                    ChangeInNetIncome = key['changeInNetIncome']
                    CapitalExpenditures = key['capitalExpenditures']
                    ChangeInReceivables = key['changeInReceivables']
                    ChangeInExchangeRate = key['changeInExchangeRate']
                    ChangeInCashAndCashEquivalents = key['changeInCashAndCashEquivalents']

                    preparedJsonList.append([Symbol, FilingType, FiscalDateEnding, ReportedCurrency, Investments, ChangeInLiabilities, CashflowFromInvestment, OtherCashflowFromInvestment, NetBorrowings, CashflowFromFinancing, OtherCashflowFromFinancing, ChangeInOperatingActivities, NetIncome,
                                             ChangeInCash, OperatingCashflow, OtherOperatingCashflow, Depreciation, DividendPayout, StockSaleAndPurchase, ChangeInInventory, ChangeInAccountReceivables, ChangeInNetIncome, CapitalExpenditures, ChangeInReceivables, ChangeInExchangeRate, ChangeInCashAndCashEquivalents])
                except TypeError:
                    self.SwapFiles(symbol)
                    Logger.LogError(
                        f"Needs to be pulled again {symbol}.")
                    break

        if self.eJsonFolderContext == EJsonFolder.ANNUALBALANCE or self.eJsonFolderContext == EJsonFolder.QUARTERLYBALANCE:

            for key in jsonData:

                try:
                    Symbol = symbol
                    FilingType = "A" if "annual" in self.eJsonFolderContext.value else "Q"

                    FiscalDateEnding = key['fiscalDateEnding']
                    ReportedCurrency = key['reportedCurrency']
                    TotalAssets = key['totalAssets']
                    IntangibleAssets = key['intangibleAssets']
                    EarningAssets = key['earningAssets']
                    OtherCurrentAssets = key['otherCurrentAssets']
                    TotalLiabilities = key['totalLiabilities']
                    TotalShareholderEquity = key['totalShareholderEquity']
                    DeferredLongTermLiabilities = key['deferredLongTermLiabilities']
                    OtherCurrentLiabilities = key['otherCurrentLiabilities']
                    CommonStock = key['commonStock']
                    RetainedEarnings = key['retainedEarnings']
                    OtherLiabilities = key['otherLiabilities']
                    Goodwill = key['goodwill']
                    OtherAssets = key['otherAssets']
                    Cash = key['cash']
                    TotalCurrentLiabilities = key['totalCurrentLiabilities']
                    ShortTermDebt = key['shortTermDebt']
                    CurrentLongTermDebt = key['currentLongTermDebt']
                    OtherShareholderEquity = key['otherShareholderEquity']
                    PropertyPlantEquipment = key['propertyPlantEquipment']
                    TotalCurrentAssets = key['totalCurrentAssets']
                    LongTermInvestments = key['longTermInvestments']
                    NetTangibleAssets = key['netTangibleAssets']
                    ShortTermInvestments = key['shortTermInvestments']
                    NetReceivables = key['netReceivables']
                    LongTermDebt = key['longTermDebt']
                    Inventory = key['inventory']
                    AccountsPayable = key['accountsPayable']
                    TotalPermanentEquity = key['totalPermanentEquity']
                    AdditionalPaidInCapital = key['additionalPaidInCapital']
                    CommonStockTotalEquity = key['commonStockTotalEquity']
                    PreferredStockTotalEquity = key['preferredStockTotalEquity']
                    RetainedEarningsTotalEquity = key['retainedEarningsTotalEquity']
                    TreasuryStock = key['treasuryStock']
                    AccumulatedAmortization = key['accumulatedAmortization']
                    OtherNonCurrrentAssets = key['otherNonCurrrentAssets']
                    DeferredLongTermAssetCharges = key['deferredLongTermAssetCharges']
                    TotalNonCurrentAssets = key['totalNonCurrentAssets']
                    CapitalLeaseObligations = key['capitalLeaseObligations']
                    TotalLongTermDebt = key['totalLongTermDebt']
                    OtherNonCurrentLiabilities = key['otherNonCurrentLiabilities']
                    TotalNonCurrentLiabilities = key['totalNonCurrentLiabilities']
                    NegativeGoodwill = key['negativeGoodwill']
                    Warrants = key['warrants']
                    PreferredStockRedeemable = key['preferredStockRedeemable']
                    CapitalSurplus = key['capitalSurplus']
                    LiabilitiesAndShareholderEquity = key['liabilitiesAndShareholderEquity']
                    CashAndShortTermInvestments = key['cashAndShortTermInvestments']
                    AccumulatedDepreciation = key['accumulatedDepreciation']
                    CommonStockSharesOutstanding = key['commonStockSharesOutstanding']

                    preparedJsonList.append([Symbol, FilingType, FiscalDateEnding, ReportedCurrency, TotalAssets, IntangibleAssets, EarningAssets, OtherCurrentAssets, TotalLiabilities, TotalShareholderEquity, DeferredLongTermLiabilities, OtherCurrentLiabilities, CommonStock, RetainedEarnings, OtherLiabilities, Goodwill, OtherAssets, Cash, TotalCurrentLiabilities, ShortTermDebt, CurrentLongTermDebt, OtherShareholderEquity, PropertyPlantEquipment, TotalCurrentAssets, LongTermInvestments, NetTangibleAssets, ShortTermInvestments, NetReceivables, LongTermDebt, Inventory, AccountsPayable,
                                             TotalPermanentEquity, AdditionalPaidInCapital, CommonStockTotalEquity, PreferredStockTotalEquity, RetainedEarningsTotalEquity, TreasuryStock, AccumulatedAmortization, OtherNonCurrrentAssets, DeferredLongTermAssetCharges, TotalNonCurrentAssets, CapitalLeaseObligations, TotalLongTermDebt, OtherNonCurrentLiabilities, TotalNonCurrentLiabilities, NegativeGoodwill, Warrants, PreferredStockRedeemable, CapitalSurplus, LiabilitiesAndShareholderEquity, CashAndShortTermInvestments, AccumulatedDepreciation, CommonStockSharesOutstanding])
                except TypeError:
                    self.SwapFiles(symbol)
                    Logger.LogError(
                        f"Needs to be pulled again {symbol}.")
                    break

        if self.eJsonFolderContext == EJsonFolder.ANNUALCASH or self.eJsonFolderContext == EJsonFolder.QUARTERLYCASH:

            for key in jsonData:

                try:
                    Symbol = symbol
                    FilingType = "A" if "annual" in self.eJsonFolderContext.value else "Q"
                    FiscalDateEnding = key['fiscalDateEnding']
                    ReportedCurrency = key['reportedCurrency']
                    TotalRevenue = key['totalRevenue']
                    TotalOperatingExpense = key['totalOperatingExpense']
                    CostOfRevenue = key['costOfRevenue']
                    GrossProfit = key['grossProfit']
                    Ebit = key['ebit']
                    NetIncome = key['netIncome']
                    ResearchAndDevelopment = key['researchAndDevelopment']
                    EffectOfAccountingCharges = key['effectOfAccountingCharges']
                    IncomeBeforeTax = key['incomeBeforeTax']
                    MinorityInterest = key['minorityInterest']
                    SellingGeneralAdministrative = key['sellingGeneralAdministrative']
                    OtherNonOperatingIncome = key['otherNonOperatingIncome']
                    OperatingIncome = key['operatingIncome']
                    OtherOperatingExpense = key['otherOperatingExpense']
                    InterestExpense = key['interestExpense']
                    TaxProvision = key['taxProvision']
                    InterestIncome = key['interestIncome']
                    NetInterestIncome = key['netInterestIncome']
                    ExtraordinaryItems = key['extraordinaryItems']
                    NonRecurring = key['nonRecurring']
                    OtherItems = key['otherItems']
                    IncomeTaxExpense = key['incomeTaxExpense']
                    TotalOtherIncomeExpense = key['totalOtherIncomeExpense']
                    DiscontinuedOperations = key['discontinuedOperations']
                    NetIncomeFromContinuingOperations = key['netIncomeFromContinuingOperations']
                    NetIncomeApplicableToCommonShares = key['netIncomeApplicableToCommonShares']
                    PreferredStockAndOtherAdjustments = key['preferredStockAndOtherAdjustments']

                    preparedJsonList.append([Symbol, FilingType, FiscalDateEnding, ReportedCurrency, TotalRevenue, TotalOperatingExpense, CostOfRevenue, GrossProfit, Ebit, NetIncome, ResearchAndDevelopment, EffectOfAccountingCharges, IncomeBeforeTax, MinorityInterest, SellingGeneralAdministrative, OtherNonOperatingIncome, OperatingIncome, OtherOperatingExpense, InterestExpense, TaxProvision, InterestIncome, NetInterestIncome, ExtraordinaryItems, NonRecurring, OtherItems, IncomeTaxExpense,
                                             TotalOtherIncomeExpense, DiscontinuedOperations, NetIncomeFromContinuingOperations, NetIncomeApplicableToCommonShares, PreferredStockAndOtherAdjustments])

                except TypeError:
                    self.SwapFiles(symbol)
                    Logger.LogError(
                        f"Needs to be pulled again {symbol}.")
                    break

        return self.TransformValues(preparedJsonList)

    def TransformValues(self, preparedJsonList: list):
        finalPreparedList = []
        for listOfValues in preparedJsonList:
            for count, value in enumerate(listOfValues):
                listOfValues[count] = None if value == "None" else value
            finalPreparedList.append(tuple(listOfValues))
        return tuple(finalPreparedList)

    def InsertDataFromJsonMany(self, preparedJsonTuple: tuple):
        sqlStatements = [
            """INSERT INTO CompanyOverview (Symbol, Currency, AssetType, Name, Description, Exchange, Country, Sector, Industry) Values (?,?,?,?,?,?,?,?,?)""",

            """INSERT INTO HistoricPriceData (Symbol, Date, OpenPrice, HighPrice, LowPrice,ClosePrice,Volume) VALUES (?,?,?,?,?,?,?)""",

            """INSERT INTO IncomeStatements (Symbol, FilingType, Date, Currency, Investments, ChangeInLiabilities, CashflowFromInvestment, OtherCashflowFromInvestment, NetBorrowings, CashflowFromFinancing, OtherCashflowFromFinancing, ChangeInOperatingActivities, NetIncome, ChangeInCash, OperatingCashflow, OtherOperatingCashflow, Depreciation, DividendPayout, StockSaleAndPurchase, ChangeInInventory, ChangeInAccountReceivables, ChangeInNetIncome, CapitalExpenditures, ChangeInReceivables, ChangeInExchangeRate, ChangeInCashAndCashEquivalents) Values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",

            """INSERT INTO BalanceSheetStatements (Symbol, FilingType, Date, Currency, TotalAssets, IntangibleAssets, EarningAssets, OtherCurrentAssets, TotalLiabilities, TotalShareholderEquity, DeferredLongTermLiabilities, OtherCurrentLiabilities, CommonStock, RetainedEarnings, OtherLiabilities, Goodwill, OtherAssets, Cash, TotalCurrentLiabilities, ShortTermDebt, CurrentLongTermDebt, OtherShareholderEquity, PropertyPlantEquipment, TotalCurrentAssets, LongTermInvestments, NetTangibleAssets, ShortTermInvestments, NetReceivables, LongTermDebt, Inventory, AccountsPayable, TotalPermanentEquity, AdditionalPaidInCapital, CommonStockTotalEquity, PreferredStockTotalEquity, RetainedEarningsTotalEquity, TreasuryStock, AccumulatedAmortization, OtherNonCurrrentAssets, DeferredLongTermAssetCharges, TotalNonCurrentAssets, CapitalLeaseObligations, TotalLongTermDebt, OtherNonCurrentLiabilities, TotalNonCurrentLiabilities, NegativeGoodwill, Warrants, PreferredStockRedeemable, CapitalSurplus, LiabilitiesAndShareholderEquity, CashAndShortTermInvestments, AccumulatedDepreciation, CommonStockSharesOutstanding) Values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",

            """INSERT INTO CashFlowStatements (Symbol, FilingType, Date, Currency, TotalRevenue, TotalOperatingExpense, CostOfRevenue, GrossProfit, EBIT, NetIncome, ResearchAndDevelopment, EffectOfAccountingCharges, IncomeBeforeTax, MinorityInterest, SellingGeneralAdministrative, OtherNonOperatingIncome, OperatingIncome, OtherOperatingExpense, InterestExpense, TaxProvision, InterestIncome, NetInterestIncome, ExtraordinaryItems, NonRecurring, OtherItems, IncomeTaxExpense, TotalOtherIncomeExpense, DiscontinuedOperations, NetIncomeFromContinuingOperations, NetIncomeApplicableToCommonShares, PreferredStockAndOtherAdjustments) Values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"""
        ]
        sql = ''
        if self.eJsonFolderContext == EJsonFolder.OVERVIEW:
            sql = sqlStatements[0]
        if self.eJsonFolderContext == EJsonFolder.PRICES:
            sql = sqlStatements[1]
        if self.eJsonFolderContext == EJsonFolder.ANNUALINCOME or self.eJsonFolderContext == EJsonFolder.QUARTERLYINCOME:
            sql = sqlStatements[2]
        if self.eJsonFolderContext == EJsonFolder.ANNUALBALANCE or self.eJsonFolderContext == EJsonFolder.QUARTERLYBALANCE:
            sql = sqlStatements[3]
        if self.eJsonFolderContext == EJsonFolder.ANNUALCASH or self.eJsonFolderContext == EJsonFolder.QUARTERLYCASH:
            sql = sqlStatements[4]

        self.ExecuteSql(sql, preparedJsonTuple)

    def ExecuteSql(self, sql: str, preparedJsonTuple: tuple):

        if len(preparedJsonTuple) != 0:
            try:
                self.__cursor__.executemany(sql, preparedJsonTuple)

                self.__connection__.commit()

                Logger.LogInfo(
                    f"Inserted {preparedJsonTuple}")
            except pyodbc.Error as ex:

                Logger.LogError(
                    f"failed to insert {preparedJsonTuple} {ex}")

    def SwapFiles(self, symbol: str):
        oldJsonFilePath = f"{PathHelper.JsonRoot()}\\{self.eJsonFolderContext.value}\\done\\{symbol}.json"
        newJsonFilePath = f"{PathHelper.JsonRoot()}\\{self.eJsonFolderContext.value}\\redo\\{symbol}.json"
        os.replace(oldJsonFilePath, newJsonFilePath)
