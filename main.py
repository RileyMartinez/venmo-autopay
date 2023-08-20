import os
import traceback
import logging
from dotenv import load_dotenv
from enums.TransactionType import TransactionType
from models.payment import Payment
from models.request import Request
from venmo import Venmo
from smtp_client import SmtpClient
from datetime import datetime

def main() -> None:
    try:
        load_dotenv()

        logging.basicConfig(
            filename='main.log', 
            filemode='a', 
            level=logging.INFO, 
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        venmo = Venmo(os.getenv('VENMO_ACCESS_TOKEN'))

        smtp = SmtpClient(
            os.getenv('SMTP_USERNAME'), 
            os.getenv('SMTP_PASSWORD'), 
            os.getenv('SMTP_SERVER'), 
            os.getenv('SMTP_PORT'))
        
        payments: list[Payment] = get_payments()
        requests: list[Request] = get_requests()

        for payment in payments:
            success = venmo.send_money(
                payment.amount,
                payment.note,
                payment.target_user_id,
                payment.funding_source_id)

            log_transaction(smtp, TransactionType.PAYMENT, success, payment.target_user_id)
        
        for request in requests:
            success = venmo.request_money(
                request.amount,
                request.note,
                request.target_user_id)

            log_transaction(smtp, TransactionType.REQUEST, success, request.target_user_id)

    except Exception as e:
        logging.error(f'An exception was thrown')
        send_error_notification(smtp, e)

def send_error_notification(smtp: SmtpClient, e: Exception) -> None:
    smtp.send_email(
            os.getenv('SMTP_TO'),
            os.getenv('SMTP_SUBJECT'),
            f'Failed Transaction\n\nError:\n{e}\n\nDetails:\n{traceback.format_exc()}')

def log_transaction(smtp: SmtpClient, transactionType: TransactionType, success: bool, target_user_id: int) -> None:
    if success:
        logging.info(f'Venmo {transactionType.to_lower()} successful to User ID: {mask_string(str(target_user_id))}')                 
    else:
        logging.error(f'Venmo {transactionType.to_lower()} failed to User ID: {mask_string(str(target_user_id))}')

        smtp.send_email(
                    os.getenv('SMTP_TO'),
                    os.getenv('SMTP_SUBJECT'),
                    f'Venmo {transactionType.to_lower()} failed to User ID: {target_user_id}')

def mask_string(s: str) -> str:
    return 'X' * (len(s) - 4) + s[-4:]

def get_payments() -> list[Payment]:
    payments: list[Payment] = []
    i: int = 1

    while True:
        amount: str = os.getenv(f'VENMO_PAYMENT_AMOUNT_{i}')
        note: str = os.getenv(f'VENMO_PAYMENT_NOTE_{i}')
        target_user_id: str = os.getenv(f'VENMO_PAYMENT_USER_ID_{i}')
        funding_source_id: str = os.getenv('VENMO_FUNDING_SOURCE_ID')

        if not all([amount, note, target_user_id, funding_source_id]):
            break

        payment: Payment = Payment(
            float(amount),
            f'{note}{datetime.now().strftime("%m/%d/%y")}',
            int(target_user_id),
            int(funding_source_id)
        )

        payments.append(payment)
        i += 1
    
    return payments

def get_requests() -> list[Request]:
    requests: list[Request] = []
    i: int = 1

    while True:
        amount: str = os.getenv(f'VENMO_REQUEST_AMOUNT_{i}')
        note: str = os.getenv(f'VENMO_REQUEST_NOTE_{i}')
        target_user_id: str = os.getenv(f'VENMO_REQUEST_USER_ID_{i}')

        if not all([amount, note, target_user_id]):
            break

        request: Request = Request(
            float(amount),
            f'{note}{datetime.now().strftime("%m/%d/%y")}',
            int(target_user_id)
        )

        requests.append(request)
        i += 1
    
    return requests

if __name__ == '__main__':
    main()
