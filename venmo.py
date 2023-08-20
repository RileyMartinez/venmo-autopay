from venmo_api import Client, PaymentMethod, User

class Venmo:
    client: Client

    def __init__(self, access_token: str) -> None:
        self.client = Client(access_token=access_token)

    def get_user_id_by_username(self, username: str) -> str:
        user: User = self.client.user.get_user_by_username(username)
        return user.id

    def get_payment_methods(self) -> list[PaymentMethod]:
        return self.client.payment.get_payment_methods()

    def send_money(self, amount: float, note: str, target_user_id: int, funding_source_id: int) -> bool:
        return self.client.payment.send_money(amount, note, target_user_id, funding_source_id)

    def request_money(self, amount: float, note: str, target_user_id: int) -> bool:
        return self.client.payment.request_money(amount, note, target_user_id)