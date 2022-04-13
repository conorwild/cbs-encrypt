import sys
import os
from cryptography.fernet import Fernet

key = input("Enter your key: ")
cipher = Fernet(key)

filename = sys.argv[1]
print(f"Decrypting: {filename} ...")

with open(filename, 'rb') as rf:
    e_file = rf.read()

decrypted_data = cipher.decrypt(e_file)

path, file = os.path.split(filename)
d_filename = os.path.join(path, file[10:])
with open(d_filename, 'wb') as wf:
    wf.write(decrypted_data)

print('DONE')