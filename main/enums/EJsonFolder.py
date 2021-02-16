from enum import Enum, unique


@unique
class EJsonFolder(Enum):

    ANNUAL = 'annual-earnings-dates'
    QUARTERLY = 'quarterly-earnings-dates'
    PRICES = 'prices'
    REDO = 'redo'
    DONE = 'done'
    NONE = ''

    def describe(self):
        # self is the member here
        return self.name, self.value

    def __str__(self):
        return 'my custom str! {0}'.format(self.value)
