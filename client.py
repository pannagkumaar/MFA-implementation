import socket
import pyotp

HOST = '127.0.0.1'
PORT = 12345

def send_request(data):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((HOST, PORT))
            print("Connection established")

            client_socket.sendall(str(data).encode('utf-8'))
            print("Request sent")

            response = client_socket.recv(1024)
            print(response.decode('utf-8'))

    except ConnectionRefusedError:
        print("Error: Connection to the server was refused. Make sure the server is running.")
    except Exception as e:
        print(f"Error: {e}")

def login():
    try:
        username = input("Enter your username: ")
        password = input("Enter your password: ")

        # For simplicity, use hardcoded values (replace with user input or database retrieval)
        otp_secret = 'apple'  # Replace with the actual secret key from the server
        totp = pyotp.TOTP(otp_secret)
        otp_code = totp.now()

        data = {'action': 'login', 'username': username, 'password': password, 'otp_code': otp_code}
        send_request(data)

    except Exception as e:
        print(f"Error during login: {e}")

def signout():
    try:
        username = input("Enter your username: ")
        data = {'action': 'signout', 'username': username}
        send_request(data)

    except Exception as e:
        print(f"Error during sign-out: {e}")

if __name__ == '__main__':
    while True:
        print("\n1. Login")
        print("2. Sign-out")
        print("3. Exit")

        try:
            choice = input("Enter your choice (1, 2, or 3): ")

            if choice == '1':
                login()
            elif choice == '2':
                signout()
            elif choice == '3':
                print("Exiting the client.")
                break
            else:
                print("Invalid choice. Please enter 1, 2, or 3.")

        except KeyboardInterrupt:
            print("\nClient terminated by user.")
            break
        except Exception as e:
            print(f"Error: {e}")
