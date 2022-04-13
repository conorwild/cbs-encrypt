import sys
import os
from cryptography.fernet import Fernet

def main():

    key = input("Enter your key: ")

    cipher = Fernet(key)

    filename = sys.argv[1]
    print(f"Encrypting: {filename} ...")

    with open(filename, 'rb') as rf:
        e_file = rf.read()
    encrypted_data = cipher.encrypt(e_file)

    path, file = os.path.split(filename)
    e_filename = os.path.join(path, f"encrypted_{file}")
    with open(e_filename, 'wb') as wf:
        wf.write(encrypted_data)

    print('DONE')

if __name__ == '__main__':
    main()  # pylint: disable=no-value-for-parameter