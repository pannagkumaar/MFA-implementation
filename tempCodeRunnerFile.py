def generate_otp_secret():
    random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=32))
    random_string_list = list(random_string)
    random.shuffle(random_string_list)
    random_string = ''.join(random_string_list)
    return random_string