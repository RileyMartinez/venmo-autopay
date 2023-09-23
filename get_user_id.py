import os
from dotenv import load_dotenv
from clients.venmo import Venmo

def main() -> None:
    load_dotenv()
    venmo = create_venmo_client()

    while True:
        try:         
            username = input('Enter a username ("exit" to quit): ')

            if username.lower() == 'exit':
                break

            user_id = venmo.get_user_id_by_username(username)

            if user_id is not None:
                print(f'User ID: {user_id}')
            else:
                print(f'User "{username}" not found')

        except Exception as e:
            print(f'An error occurreed: {e}')

def create_venmo_client() -> Venmo:
    venmo = Venmo(os.getenv('VENMO_ACCESS_TOKEN'))
    return venmo

if __name__ == '__main__':
    main()