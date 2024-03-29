from pathlib import Path
from os import path
import argparse
from cryptography.fernet import Fernet
from io import BytesIO
import pandas as pd


class Crypt():

    @classmethod
    def request_key(cls):
        return input("Enter your key: ")

    def __init__(self, key=None, keyfile=None):
        if (key is None) & (keyfile is None):
            key = self.request_key()
        elif keyfile is not None:
            with open(keyfile, 'r') as rf:
                key = rf.read()
        self._cipher = Fernet(key)

    def encrypt(self, contents):
        return self._cipher.encrypt(contents)

    def decrypt(self, contents):
        return self._cipher.decrypt(contents)

    def encrypt_str(self, string_contents):
        contents_bytes = str.encode(string_contents, 'utf-8')
        encrypted_bytes = self.encrypt(contents_bytes)
        return encrypted_bytes.decode('utf-8')

    def decrypt_str(self, encrypted_string):
        encrypted_bytes = str.encode(encrypted_string, 'utf-8')
        decrypted_bytes = self.decrypt(encrypted_bytes)
        return decrypted_bytes.decode('utf-8')

    def encrypt_files(self, files, output_directory=None):
        files = self.check_files(files)
        for filename in files:
            print(f"Encrypting: {filename} ...")

            with open(filename, 'rb') as rf:
                e_file = rf.read()

            encrypted_data = self.encrypt(e_file)

            fp = Path(filename)
            if output_directory is None:
                output_directory = fp.parent
            Path(output_directory).mkdir(parents=True, exist_ok=True)

            e_filename = path.join(output_directory, fp.name+".crypt")
            with open(e_filename, 'wb') as wf:
                wf.write(encrypted_data)

    def decrypt_files(self, files, output_directory=None):
        files = self.check_files(files)
        for filename in files:
            print(f"Decrypting: {filename} ...")

            with open(filename, 'rb') as rf:
                e_file = rf.read()

            decrypted_data = self.decrypt(e_file)

            fp = Path(filename)
            if output_directory is None:
                output_directory = fp.parent
            Path(output_directory).mkdir(parents=True, exist_ok=True)

            d_filename = path.join(output_directory, fp.name[0:-6])
            with open(d_filename, 'wb') as wf:
                wf.write(decrypted_data)

    def decrypt_file_to_bytestream(self, filename):
        with open(filename, 'rb') as rf:
            e_file = rf.read()
        decrypted_data = self.decrypt(e_file)
        return BytesIO(decrypted_data)

    def decrypt_csv_to_pandas(self, csv_file):
        return (
            pd.read_csv(self.decrypt_file_to_bytestream(csv_file))
        )

    @classmethod
    def check_files(cls, files):
        if len(files) == 0:
            raise ValueError("No filenames provided.")
        for file in files:
            if not path.exists(file):
                raise OSError(f"{file} does not exist.")
        return files


class EncryptedData():

    def __init__(self, filename, keyfile):
        self._data = None
        self._filename = filename
        self._keyfile = keyfile

        with open(self._keyfile, 'r') as rf:
            _key = rf.read()
        self._cipher = Crypt(_key)

    @property
    def data(self):
        if self._data is None:
            self._data = (
                self._cipher.decrypt_csv_to_pandas(self._filename)
            )
        return self._data

    def reload(self):
        self._data = None


def decrypt_files_cmdline():
    parser = argparse.ArgumentParser(description='Decrypt some files.')
    parser.add_argument(
        '-o', '--output-directory', type=str,
        help='A location to save decrypted files, defaults to same directory.'
    )
    parser.add_argument(
        'files', metavar='filename', type=str, nargs='+',
        help='A file (including path) to encrypt.'
    )
    args = vars(parser.parse_args())

    Crypt().decrypt_files(args['files'], args['output_directory'])
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

    Crypt().encrypt_files(args['files'], args['output_directory'])
    print('DONE')


if __name__ == '__main__':
    encrypt_files_cmdline()  # pylint: disable=no-value-for-parameter
