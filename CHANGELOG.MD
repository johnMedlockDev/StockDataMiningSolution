# Changelog
## 0.1.2

**Additions:**

- Added batch commits with sql
  
**Changes:**
- Changed AlphaApiHandler to AlphaApiHTTP
## 0.1.1

**Additions:**

- added sql persistence.
- Added faster way to insert.
  
**Changes:**
- Extended Json Price processing to the HistoricSymbolDataGenerator.
- Refactored Logger class.
- Refactored everything.
  
**Removed**
- Enum now EJsonFolder represents all the of folders in io/json.
## 0.0.5

**Additions:**

- Added test structure - test don't work yet.
- Better error handling in AlphaAPIHandler

**Changes:**

- Refactored function GetHistoricalPriceDataFromJsonAPIAndWriteToJSONFileBatch to use GetHistoricalPriceDataFromJsonAPIAndWriteToJSONFile
- Added \_\_ properties
- Formatted doc strings

## 0.0.4

**Additions:**

- HistoricSymbolDataGenerator for api batch process management.

## 0.0.3

**Additions:**

- Get filtered list of symbols
- .env file for secrets

## 0.0.2

**Additions:**

- Gets Symbol Json in batches from a list.
- Persist Json to files.

## 0.0.1

**Additions:**

- Generate in memory list from CSV files.
- Fetch data from API
- Log errors
