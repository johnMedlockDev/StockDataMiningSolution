from enum import Enum


class EPayload(Enum):
    '''
    Enum for json payload.
    FULL = All price history.
    COMPACT = Last 100 days of price history.

    '''
    FULL = 'full'
    COMPACT = 'compact'
