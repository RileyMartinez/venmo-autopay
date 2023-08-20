class Request:
    amount: float
    note: str
    target_user_id: int

    def __init__(self, amount: float, note: str, target_user_id: int) -> None:
        self.amount = amount
        self.note = note
        self.target_user_id = target_user_id

    def __str__(self) -> str:
        return (
            f'Amount: ${self.amount}\n'
            f'Note: {self.note}\n'
            f'Target User ID: {self.target_user_id}'
        )