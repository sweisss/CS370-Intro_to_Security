"""
Seth Weiss
weissse@oregonstate.edu
CS 370 - Introduction to Security
Fall 2023
Programming Project 1 - 3.4

Description:
You are given a plaintext and a ciphertext, and you know that aes-128-cbc is used to generate 
the ciphertext from the plaintext, and you also know that the numbers in the IV are all zeros 
(not the ASCII character '0'). Another clue that you have learned is that the key used to encrypt 
this plaintext is an English word shorter than 16 characters; the word that can be found from a 
typical English dictionary. Since the word has less than 16 characters (i.e. 128 bits), space 
characters (hexadecimal value 0x20) are appended to the end of the word to form a key of 128 
bits. Your goal is to write a program to find out this key.

Cited sources:
https://canvas.oregonstate.edu/courses/1933665/pages/programming-project-encryption-helper-3-dot-4?wrap=1
https://pycryptodome.readthedocs.io/en/latest/src/cipher/classic.html#cbc-mode
"""
import sys

# from Crypto.Cipher import AES
# from Crypto.Random import get_random_bytes

import json
from base64 import b64encode, b64decode
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes

data = b"secret"
key = get_random_bytes(16)
cipher = AES.new(key, AES.MODE_CBC)
ct_bytes = cipher.encrypt(pad(data, AES.block_size))
iv = b64encode(cipher.iv).decode('utf-8')
ct = b64encode(ct_bytes).decode('utf-8')
result = json.dumps({'iv':iv, 'ciphertext':ct})
print(result)


try:
    b64 = json.loads(result)
    iv = b64decode(b64['iv'])
    ct = b64decode(b64['ciphertext'])
    cipher = AES.new(key, AES.MODE_CBC, iv)
    pt = unpad(cipher.decrypt(ct), AES.block_size)
    print("The message was: ", pt)
except (ValueError, KeyError):
    print("Incorrect decryption")



DEBUG = True



key = get_random_bytes(16)
cipher = AES.new(key, AES.MODE_CBC)
print(cipher)


# plaintext1 = 'This is a top secret.'
# print(f'paintext1: {plaintext1}') if DEBUG else 0

# ciphertextHexValuesAsString = "8d20e5056a8d24d0462ce74e4904c1b513e10d1df4a2ef2ad4540fae1ca0aaf9"
# print('Ciphertext: "', ciphertextHexValuesAsString, '"', sep="") if DEBUG else 0
# print("Data Type: ", type(ciphertextHexValuesAsString)) if DEBUG else 0

# print("Converting String to bytes...") if DEBUG else 0
# ciphertextHexValuesAsBytes = bytearray.fromhex(ciphertextHexValuesAsString)

# print('Ciphertext: "' + ''.join(format(x, '02x') for x in ciphertextHexValuesAsBytes) + '"') if DEBUG else 0



# def main():
#     param_count = len(sys.argv)

#     print(f'Num params: {param_count}') if DEBUG else 0
#     print(f'sys.argv[0]: {sys.argv[0]}') if DEBUG else 0

#     print(f'sys.argv[1]: {sys.argv[1]}') if (DEBUG and param_count > 1) else 0
#     print(f'sys.argv[2]: {sys.argv[2]}') if (DEBUG and param_count > 2) else 0


# if __name__ == "__main__":
#     main()
