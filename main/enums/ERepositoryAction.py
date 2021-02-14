from enum import Enum


class ERepositoryAction(Enum):
    """This delegates which repository should be inspected for flitered list creation.
    PRICES = Creates a list against the symbols in the prices folder.
    EARNINGS = Creates a list against the symbols in the annual-earnings-dates folder.

    """
    PRICES = "prices"
    EARNINGS = "annual-earnings-dates"
