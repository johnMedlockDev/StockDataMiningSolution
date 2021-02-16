from enum import Enum, unique


@unique
class EPayload(Enum):

    FULL = 'full'
    COMPACT = 'compact'

    def describe(self):
        # self is the member here
        return self.name, self.value

    def __str__(self):
        return 'my custom str! {0}'.format(self.value)
