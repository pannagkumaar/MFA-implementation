import socket
import string
import random
from prime import primitive_root, getLowLevelPrime, isMillerRabinPassed
import pyotp
import time
import threading
import json
signed_in_users = {}
active_connections = 0

HOST = '127.0.0.1'
PORT = 12345
MAX_ACTIVE_CONNECTIONS = 2  # Allow more than one connection

users=open("users.json","r+")
def generate_otp_secret():
    random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=32))
    random_string_list = list(random_string)
    random.shuffle(random_string_list)
    random_string = ''.join(random_string_list)
    return random_string
def refresh_secret_key(users_file="users.json"):
    with open(users_file, "r+") as file:
        users_data = json.load(file)

        for user in users_data:
            generated_otp_secret = generate_otp_secret()
            users_data[user]['otp_secret'] = generated_otp_secret
            print(f"New OTP secret for user {user}: {generated_otp_secret}")
        file.seek(0)
        file.truncate()
        json.dump(users_data, file)
    time.sleep(100)


    

def check_user_exists(username):
    return username in users



def handle_login(conn, data):
    global active_connections
    global signed_in_users
    username = data.get('username')
    password = data.get('password')
    otp_code = data.get('otp_code')

    print(f"Attempting login for user: {username}")

    if active_connections >= MAX_ACTIVE_CONNECTIONS:
        conn.sendall(b'Server reached maximum active connections. Please try again later.\n')
        conn.close()
        return

    if signed_in_users.get(username):
        print(f"User {username} already signed in. Closing connection.")
        conn.sendall(b'Another user is already signed in. Please sign out first.\n')
        conn.close()
        return

    if check_user_exists(username) and users[username]['password'] == password:
        
        totp =pyotp.TOTP(users[username]['otp_secret'])
        if totp.verify(otp_code):
            signed_in_users[username] = True
            active_connections += 1
            conn.sendall(b'Login successful!\n')
            print(f"Login successful for user: {username}")
        else:
            conn.sendall(b'Invalid OTP code\n')
            print(f"Invalid OTP code for user: {username}")
    else:
        conn.sendall(b'Invalid credentials\n')
        print(f"Invalid credentials for user: {username}")

    # Do not close the connection here, allow for subsequent connections

def handle_signout(conn, data):
    global active_connections
    global signed_in_users
    username = data.get('username')
     
    print(f"Attempting sign-out for user: {username}")

    if signed_in_users.get(username):
        
        conn.sendall(b'Sign-out successful!\n')
        signed_in_users.pop(username)
        active_connections -= 1
        print(f"Sign-out successful for user: {username}")
    else:
        conn.sendall(b'No user is currently signed in.\n')
        print(f"No user is currently signed in for user: {username}")

    
def send_key(conn):
    def get_prime_and_base():
        while True:
            n = 20
            prime_candidate = getLowLevelPrime(n)
            if not isMillerRabinPassed(prime_candidate):
                continue
            else:
                base = primitive_root(prime_candidate)
                return prime_candidate, base
    def diffie_hellman():
        prime, base = get_prime_and_base()
        private_key = random.randint(2, prime - 2)
        public_key = (base ** private_key) % prime
        return prime, base, private_key, public_key
    
    def encrypt_string(string, key):
        encrypted_string = ""
        for char in string:
            encrypted_char = chr(ord(char) + key)
            encrypted_string += encrypted_char
        return encrypted_string
    def calculate_shared_secret_key(public_key, private_key, prime):
        print("Received client public key:", public_key)
        return (public_key ** private_key) % prime

    def server(conn):
        prime, base, private_key, public_key = diffie_hellman()
        
        conn.send(str(prime).encode())
        conn.send(str(base).encode())
        client_public_key = int(conn.recv(1024).decode())
        print("Received client public key:", client_public_key)
        conn.send(str(public_key).encode())

        shared_secret_key = calculate_shared_secret_key(client_public_key, private_key, prime)
        print("Shared Secret Key:", shared_secret_key)

        string_to_send = "abcdefghijklmnopqrstuvwxyz"
        
        encrypted_string = encrypt_string(string_to_send, shared_secret_key)
        
        conn.send(encrypted_string.encode())
            
        

    server(conn)    
def main():
    refresh_thread = threading.Thread(target=refresh_secret_key)
    refresh_thread.start()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen()

        print(f'Server listening on {HOST}:{PORT}')
        conn, addr = server_socket.accept()
        print(f'Connected by {addr}')
        send_key(conn)

        while True:
            if active_connections < MAX_ACTIVE_CONNECTIONS:
                print("Waiting for connection...")

                conn, addr = server_socket.accept()
                with conn:
                    print("Connection accepted")

                    data = conn.recv(1024)
                    if not data:
                        print("No data received")

                    data_dict = eval(data.decode('utf-8'))
                    action = data_dict.get('action', '')

                    if action == 'login':
                        handle_login(conn, data_dict)
                    elif action == 'signout':
                        handle_signout(conn, data_dict)
                    else:
                        conn.sendall(b'Invalid action\n')
                        conn.close()

if __name__ == '__main__':
    main()
