import base64
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


def main():
    password_str = input("Enter your password: ")
    password = password_str.encode("utf-8")

    my_salt = input("Enter your salt: ")
    assert len(my_salt) == 32

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=my_salt.encode("utf-8"),
        iterations=100000,
        backend=default_backend(),
    )

    key = base64.urlsafe_b64encode(kdf.derive(password))
    print(key.decode())


if __name__ == "__main__":
    main()  # pylint: disable=no-value-for-parameter
