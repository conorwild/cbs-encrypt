from argparse import ArgumentError
import sys
import os
from cryptography.fernet import Fernet
from io import BytesIO

def ask_for_key():
    return input("Enter your key: ")

def encrypt_files(files):
    cipher = Fernet(ask_for_key())

    for filename in files:
        print(f"Encrypting: {filename} ...")

        with open(filename, 'rb') as rf:
            e_file = rf.read()
        encrypted_data = cipher.encrypt(e_file)

        e_filename = filename + ".crypt"
        with open(e_filename, 'wb') as wf:
            wf.write(encrypted_data)



def decrypt_files(files):
    cipher = Fernet(ask_for_key())

    for filename in files:
        print(f"Decrypting: {filename} ...")

        with open(filename, 'rb') as rf:
            e_file = rf.read()

        decrypted_data = cipher.decrypt(e_file)

        d_filename = filename[:-6]  # stripts ".crypt"
        with open(d_filename, 'wb') as wf:
            wf.write(decrypted_data)

def decrypt_file_to_bytestream(filename, key=None):
    if key is None:
        key = ask_for_key()
    cipher = Fernet(key)
    with open(filename, 'rb') as rf:    
        e_file = rf.read()
    decrypted_data = cipher.decrypt(e_file)
    return BytesIO(decrypted_data)

def check_files(files):
    if len(files) == 0:
        raise ValueError("No filenames provided.")
    return files

def decrypt_files_cmdline():
    files = sys.argv[1:]
    decrypt_files(check_files(files))
    print('DONE')

def encrypt_files_cmdline():
    files = sys.argv[1:]
    encrypt_files(check_files(files))
    print('DONE')



