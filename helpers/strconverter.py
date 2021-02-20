strList = ["fiscalDateEnding","reportedCurrency","investments","changeInLiabilities","cashflowFromInvestment","otherCashflowFromInvestment","netBorrowings","cashflowFromFinancing","otherCashflowFromFinancing","changeInOperatingActivities","netIncome","changeInCash","operatingCashflow","otherOperatingCashflow","depreciation","dividendPayout","stockSaleAndPurchase","changeInInventory","changeInAccountReceivables","changeInNetIncome","capitalExpenditures","changeInReceivables","changeInExchangeRate","changeInCashAndCashEquivalents"]

print(len(strList))
print("")
listLen = len(strList)
for count, value in enumerate(strList):
    newthing = ''
    for t in value:
        newthing = value.replace(t, t.capitalize(), 1)
        strList[count] = newthing
        break

    print(f"{newthing} [decimal](30, 0) NULL,")

print("")

newListStr = str(strList).replace("'", "").replace("[", "(").replace("]", ")")

print(newListStr)


print("")

marks = "("

for _ in strList:
    marks += "?,"
marks += ")"

sql = f"""INSERT INTO  {newListStr} Values {marks}"""


print(sql)
