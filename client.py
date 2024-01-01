import socket
import pyotp
import os
from dotenv import load_dotenv
import random
import time

HOST = '127.0.0.1'
PORT = 12345




def dh_secret(conn):
    def diffie_hellman(prime,base):
    
        private_key = random.randint(2, prime - 2)
        public_key = (base ** private_key) % prime
        return prime, base, private_key, public_key

    def calculate_shared_secret_key(public_key, private_key, prime):
        return (public_key ** private_key) % prime

    def decrypt_string(encrypted_string, key):
        decrypted_string = ""
        for char in encrypted_string:
            decrypted_char = chr(ord(char) - key)
            decrypted_string += decrypted_char
        return decrypted_string
    def client(conn):
        

        
        s_prime = int(conn.recv(1024).decode())
        s_base = int(conn.recv(1024).decode())
        print("Received prime:", s_prime)
        print("Received base:", s_base)
        prime, base, private_key, public_key = diffie_hellman(s_prime,s_base)

        conn.send(str(public_key).encode())
        server_public_key = int(conn.recv(1024).decode())

        shared_secret_key = calculate_shared_secret_key(server_public_key, private_key, prime)
        print("Shared Secret Key:", shared_secret_key)
        encrypted_string = conn.recv(1024).decode()

    # Decrypt the string using the shared secret key
        decrypted_string = decrypt_string(encrypted_string, shared_secret_key)
        
        return decrypted_string
    return client(conn)

def send_request(data):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((HOST, PORT))
            print("Connection established")

            client_socket.sendall(str(data).encode('utf-8'))
            print("Request sent")

            response = client_socket.recv(1024)
            print(response.decode('utf-8'))
            client_socket.close()

    except ConnectionRefusedError:
        print("Error: Connection to the server was refused. Make sure the server is running.")
    except Exception as e:
        print(f"Error: {e}")

def login(otp_secret):
    try:
        username = input("Enter your username: ")
        password = input("Enter your password: ")
            
        # For simplicity, use hardcoded values (replace with user input or database retrieval)
          # Replace with the actual secret key from the server
        totp = pyotp.TOTP(otp_secret)
        otp_code = totp.now()

        data = {'action': 'login', 'username': username, 'password': password, 'otp_code': otp_code}
        send_request(data)

    except Exception as e:
        print(f"Error during login: {e}")


#todo signout not functioning properly
def signout():
    print("Signing out...")
    # try:
    print(conn)
    username = input("Enter your username: ")
    data = {'action': 'signout', 'username': username}
    send_request(data)
    

    # except Exception as e:
    #     print(f"Error during sign-out: {e}")


if __name__ == '__main__':
    conn = None

    try:
        conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conn.connect((HOST, PORT))
        print("Connection established for secret key generation.")
    except Exception as e:
        print(f"Error: {e}")
        # Handle connection errors here

   
    otp_secret = dh_secret(conn)
    if otp_secret :
        conn.close()
        time.sleep(5)
    else:
        otp_secret=dh_secret(conn)    
    print("otp_secretkey generated and stored in .env file.", otp_secret)


    while True:
        print("\n1. Login")
        print("2. Sign-out")
        print("3. Exit")

        try:
            choice = input("Enter your choice (1, 2, or 3): ")

            if choice == '1':
                login(otp_secret)
            elif choice == '2':
                print("debug")
                signout()
            elif choice == '3':
                print("Exiting the client.")
                conn.close()
                break
            else:
                print("Invalid choice. Please enter 1, 2, or 3.")

        except KeyboardInterrupt:
            print("\nClient terminated by user.")
            break
