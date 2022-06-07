from argparse import ArgumentError
from pathlib import Path
from os import path
import sys
import argparse
import os
from cryptography.fernet import Fernet
from io import BytesIO


def ask_for_key():
    return input("Enter your key: ")


def encrypt_files(files, output_directory=None):
    cipher = Fernet(ask_for_key())

    for filename in files:
        print(f"Encrypting: {filename} ...")

        with open(filename, 'rb') as rf:
            e_file = rf.read()

        encrypted_data = cipher.encrypt(e_file)

        fp = Path(filename)
        if output_directory is None:
            output_directory = fp.parent
        Path(output_directory).mkdir(parents=True, exist_ok=True)

        e_filename = path.join(output_directory, fp.name+".crypt")
        with open(e_filename, 'wb') as wf:
            wf.write(encrypted_data)


def decrypt_files(files, output_directory=None):
    cipher = Fernet(ask_for_key())

    for filename in files:
        print(f"Decrypting: {filename} ...")

        with open(filename, 'rb') as rf:
            e_file = rf.read()

        decrypted_data = cipher.decrypt(e_file)

        fp = Path(filename)
        if output_directory is None:
            output_directory = fp.parent
        Path(output_directory).mkdir(parents=True, exist_ok=True)

        d_filename = path.join(output_directory, fp.name[0:-6])
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
    for file in files:
        if not path.exists(file):
            raise OSError(f"{file} does not exist.")
            
    return files


def decrypt_files_cmdline():
    parser = argparse.ArgumentParser(description='Decrypt some files.')
    parser.add_argument(
        '-o', '--output-directory', type=str,
        help='A location to save the decrypted files, defaults to same directory.'
    )
    parser.add_argument(
        'files', metavar='filename', type=str, nargs='+',
        help='A file (including path) to encrypt.'
    )
    args = vars(parser.parse_args())
    decrypt_files(check_files(args['files']), args['output_directory'])
    print('DONE')


def encrypt_files_cmdline():

    parser = argparse.ArgumentParser(description='Encrypt some files.')
    parser.add_argument(
        '-o', '--output-directory', type=str,
        help='A location to save encrypted files, defaults to same directory.'
    )
    parser.add_argument(
        'files', metavar='filename', type=str, nargs='+',
        help='A file (including path) to encrypt.'
    )
    args = vars(parser.parse_args())

    encrypt_files(check_files(args['files']), args['output_directory'])
    print('DONE')


if __name__ == '__main__':
    decrypt_files_cmdline()  # pylint: disable=no-value-for-parameter