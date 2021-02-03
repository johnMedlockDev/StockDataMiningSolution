from enum import Enum


class EPayload(Enum):
    """Enum for json payload.
    FULL = All price history.
    COMPACT = Last 100 days of price history.

    Args:
        Enum (Object): Base class
    """
    FULL = 'full'
    COMPACT = 'compact'
