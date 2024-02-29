from venmo_api import Client

def main() -> None:
    while True:
        try:         
            username = input('Enter Venmo username ("exit" to quit): ')

            if username.lower() == 'exit':
                break

            password = input('Enter Venmo password ("exit" to quit): ')

            if password.lower() == 'exit':
                break

            access_token = Client.get_access_token(username=username, password=password)
            print('Token: ', access_token)

        except Exception as e:
            print(f'An error occurreed: {e}')

if __name__ == '__main__':
    main()