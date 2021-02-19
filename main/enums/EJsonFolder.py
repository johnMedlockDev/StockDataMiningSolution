from enum import Enum, unique


@unique
class EJsonFolder(Enum):

    ANNUALBALANCE = 'annual-balance-sheets'
    ANNUALCASH = 'annual-cash-flows'
    ANNUALDATES = 'annual-earnings-dates'
    ANNUALINCOME = 'annual-income-statements'

    QUARTERLYBALANCE = 'quarterly-balance-sheets'
    QUARTERLYCASH = 'quarterly-cash-flows'
    QUARTERLYDATES = 'quarterly-earnings-dates'
    QUARTERLYINCOME = 'quarterly-income-statements'

    PRICES = 'prices'
    OVERVIEW = 'company-overview'

    REDO = 'redo'
    DONE = 'done'
    NONE = ''

    def describe(self):
        # self is the member here
        return self.name, self.value

    def __str__(self):
        return 'my custom str! {0}'.format(self.value)
