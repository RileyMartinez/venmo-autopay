from venmo_api import Client

class Venmo:
    def __init__(self, access_token):
        self.client = Client(access_token=access_token)

    def get_user_id_by_username(self, username):
        """Get Venmo user ID by username

        Args:
            username (string): Venmo username to query

        Returns:
            string: Venmo user ID
        """
        user = self.client.user.get_user_by_username(username)
        return user.id

    def get_payment_methods(self):
        """Get payment methods for authenticated venmo user

        Returns:
            list: List of Venmo Payment Method objects 
        """
        return self.client.payment.get_payment_methods()

    def send_money(self, amount, note, target_user_id, funding_source_id):
        """Send money to target Venmo user

        Args:
            amount (float): Amount of money to send
            note (string): Payment message
            target_user_id (string): Venmo user id to send money to
            funding_source_id (string): Venmo payment method id

        Returns:
            bool: True if transaction was successful
        """
        return self.client.payment.send_money(amount, note, target_user_id, funding_source_id)
