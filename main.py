import os
import logging
from venmo import Venmo
from smtp_client import SmtpClient
from datetime import datetime

def main():
    try:
        logging.basicConfig(
            filename='status.log', 
            filemode='a', 
            level=logging.DEBUG, 
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

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
        
        logger.info(f'Venmo payment successful to Recipient ID: {mask_string(os.getenv("VENMO_TARGET_USER_ID"))}')

        if not success:
            logger.error('Venmo payment failed')

            smtp.send_email(
                os.getenv('SMTP_TO'),
                os.getenv('SMTP_SUBJECT'),
                os.getenv('SMTP_BODY'))

    except Exception as e:
        logger.error(f'An exception was thrown')

        smtp.send_email(
            os.getenv('SMTP_TO'),
            os.getenv('SMTP_SUBJECT'),
            f'{os.getenv("SMTP_BODY")}\n\nError: {e}')

def mask_string(s):
    return 'X' * (len(s) - 4) + s[-4:]

if __name__ == '__main__':
    main()
