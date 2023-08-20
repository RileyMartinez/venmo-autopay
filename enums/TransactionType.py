from enum import Enum

class TransactionType(Enum):
    REQUEST = 1
    PAYMENT = 2

    def to_lower(self) -> str:
        return self.name.lower()
    