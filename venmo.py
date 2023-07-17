from venmo_api import Client

class Venmo:
    def __init__(self, access_token):
        self.client = Client(access_token=access_token)

    def get_user_id_by_username(self, username):
        user = self.client.user.get_user_by_username(username)
        return user.id

    def get_payment_methods(self):
        return self.client.payment.get_payment_methods()

    def send_money(self, amount, note, target_user_id, funding_source_id):
        return self.client.payment.send_money(amount, note, target_user_id, funding_source_id)
