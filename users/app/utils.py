import secrets
import string

password_length = 8


def generate_password() -> str:
    password = "".join(secrets.choice(string.ascii_lowercase + string.digits +
                       string.ascii_uppercase) for i in range(password_length))

    return password
