import socket
import pyotp

HOST = '127.0.0.1'
PORT = 12345
MAX_ACTIVE_CONNECTIONS = 2  # Allow more than one connection

users = {
    'john_doe': {
        'password': 'apple',
        'otp_secret': 'apple',
    }
}
signed_in_users = {}
active_connections = 0

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
        # conn.close()
        return

    if username in users and users[username]['password'] == password:
        totp = pyotp.TOTP(users[username]['otp_secret'])
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

    conn.close()  # Close the connection after sending the response

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen()

        print(f'Server listening on {HOST}:{PORT}')

        while True:
            if active_connections < MAX_ACTIVE_CONNECTIONS:
                print("Waiting for connection...")
                conn, addr = server_socket.accept()
                print(f'Connected by {addr}')

                with conn:
                    print("Connection accepted")

                    data = conn.recv(1024)
                    if not data:
                        break

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
