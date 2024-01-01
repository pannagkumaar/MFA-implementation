import random 
import string
import json
import time

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
            time.sleep(10)

        file.seek(0)
        file.truncate()
        json.dump(users_data, file)

refresh_secret_key()
