import os
import traceback
import logging
from typing import Union
from dotenv import load_dotenv
from models.payment import Payment
from models.request import Request
from venmo import Venmo
from smtp_client import SmtpClient
from datetime import datetime

def main() -> None:
    try:
        load_dotenv()
        configure_logging()
        venmo = create_venmo_client()
        smtp = create_smtp_client()        
        send_payments(venmo, smtp)       
        send_requests(venmo, smtp)

    except Exception as e:
        send_error_notification(smtp, e)

def create_venmo_client() -> Venmo:
    venmo = Venmo(os.getenv('VENMO_ACCESS_TOKEN'))
    return venmo

def configure_logging() -> None:
    logging.basicConfig(
            filename='main.log', 
            filemode='a', 
            level=logging.INFO, 
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def create_smtp_client() -> SmtpClient:
    smtp = SmtpClient(
            os.getenv('SMTP_USERNAME'), 
            os.getenv('SMTP_PASSWORD'), 
            os.getenv('SMTP_SERVER'), 
            int(os.getenv('SMTP_PORT')))
        
    return smtp

def send_requests(venmo, smtp) -> None:
    requests: list[Request] = get_requests()
            
    for request in requests:
        success = venmo.request_money(
                request.amount,
                request.note,
                request.target_user_id)

        send_transaction_notification(smtp, success, request)

def send_payments(venmo, smtp) -> None:
    payments: list[Payment] = get_payments()

    for payment in payments:
        success = venmo.send_money(
                payment.amount,
                payment.note,
                payment.target_user_id,
                payment.funding_source_id)

        send_transaction_notification(smtp, success, payment)

def send_error_notification(smtp: SmtpClient, e: Exception) -> bool:
    logging.error(f'An exception was thrown')

    return smtp.send_email(
            os.getenv('SMTP_TO'),
            os.getenv('SMTP_SUBJECT'),
            f'Failed Transaction\n\nError:\n{e}\n\nDetails:\n{traceback.format_exc()}')

def send_transaction_notification(smtp: SmtpClient, success: bool, transaction: Union[Payment, Request]) -> bool:
    transaction_name: str = transaction.__class__.__name__.lower()
    log_message: str = f'{success} | Venmo {transaction_name} to User ID: {mask_string(str(transaction.target_user_id))}'
    email_body: str = f'Venmo {transaction_name} {success}:\n\n{transaction}'

    if success:
        logging.info(log_message)

        return smtp.send_email(
            os.getenv('SMTP_TO'),
            os.getenv('SMTP_SUBJECT'),
            email_body
        )                 
    else:
        logging.error(log_message)

        return smtp.send_email(
            os.getenv('SMTP_TO'),
            os.getenv('SMTP_SUBJECT'),
            email_body
        )

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

def mask_string(s: str) -> str:
    return 'X' * (len(s) - 4) + s[-4:]

if __name__ == '__main__':
    main()
