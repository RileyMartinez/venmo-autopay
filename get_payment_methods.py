import os
from dotenv import load_dotenv
from clients.venmo import Venmo

def main() -> None:
    load_dotenv()
    venmo = create_venmo_client()
    payment_methods = venmo.get_payment_methods()

    for method in payment_methods:
        print('============================')
        print(f'ID: {method.id}')
        print(f'Name: {method.name}')
        print(f'Role: {method.role}')
        print(f'Type: {method.type}')

def create_venmo_client() -> Venmo:
    venmo = Venmo(os.getenv('VENMO_ACCESS_TOKEN'))
    return venmo

if __name__ == '__main__':
    main()