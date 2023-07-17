import os
from venmo import Venmo
from smtp_client import SmtpClient
from dotenv import load_dotenv
from datetime import datetime

def main():
    try:
        load_dotenv()

        venmo = Venmo(os.getenv('VENMO_ACCESS_TOKEN'))

        smtp = SmtpClient(
            os.getenv('SMTP_USERNAME'), 
            os.getenv('SMTP_PASSWORD'), 
            os.getenv('SMTP_SERVER'), 
            os.getenv('SMTP_PORT'))

        success = venmo.send_money(
            float(os.getenv('VENMO_PAYMENT_AMOUNT')),
            f'{os.getenv("VENMO_PAYMENT_NOTE")} {datetime.now().strftime("%m/%d/%y")}',
            os.getenv('VENMO_TARGET_USER_ID'),
            os.getenv('VENMO_FUNDING_SOURCE_ID'))

        if not success:
            smtp.send_email(
                os.getenv('SMTP_TO'),
                os.getenv('SMTP_SUBJECT'),
                os.getenv('SMTP_BODY'))

    except Exception as e:
        smtp.send_email(
            os.getenv('SMTP_TO'),
            os.getenv('SMTP_SUBJECT'),
            f'{os.getenv("SMTP_BODY")}\n\nError: {e}')

main()
