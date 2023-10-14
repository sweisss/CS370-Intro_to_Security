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
https://stackoverflow.com/questions/7585435/best-way-to-convert-string-to-bytes-in-python-3
"""
import sys

# from Crypto.Cipher import AES
# from Crypto.Random import get_random_bytes

import json
from base64 import b64encode, b64decode
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes

# data = b"secret"
# # key = get_random_bytes(16)
# key = pad(b'key1', AES.block_size)
# print(f'Key: {key}')
# cipher = AES.new(key, AES.MODE_CBC)
# ct_bytes = cipher.encrypt(pad(data, AES.block_size))
# iv = b64encode(cipher.iv).decode('utf-8')
# ct = b64encode(ct_bytes).decode('utf-8')
# result = json.dumps({'iv':iv, 'ciphertext':ct})
# print(result)


# try:
#     b64 = json.loads(result)
#     iv = b64decode(b64['iv'])
#     ct = b64decode(b64['ciphertext'])
#     cipher = AES.new(key, AES.MODE_CBC, iv)
#     pt = unpad(cipher.decrypt(ct), AES.block_size)
#     print("The message was: ", pt)
# except (ValueError, KeyError):
#     print("Incorrect decryption")

PLAINTEXT = "This is a top secret."
CIPHER_STR = "8d20e5056a8d24d0462ce74e4904c1b513e10d1df4a2ef2ad4540fae1ca0aaf9"
CIPHER_HEX = bytearray.fromhex(CIPHER_STR)
MAX_KEY_LEN = 15
DEBUG = True

debug_print = lambda input: print(input) if DEBUG else 0


# key = get_random_bytes(16)
# cipher = AES.new(key, AES.MODE_CBC)


# plaintext1 = b'This is a top secret.'
# debug_print(f'paintext1: {plaintext1}')

# text = 'text example'
# print(text)
# text2 = text.encode('utf-8')
# print(text2)



def load_key_words(file: str) -> list:
    with open(file, 'r') as f:
        words = f.readlines()

    return words


def filter_words(words: list, wordlen: int) -> list:
    small_words = [word.strip() for word in words if len(word) <= wordlen]
    debug_print(f'Words in words.txt: {len(words)}')
    debug_print(f'Words less than 16 chars in words.txt: {len(small_words)}')

    return small_words


def main():
    words = load_key_words('./words.txt')
    small_words = filter_words(words, MAX_KEY_LEN)

    first_word = small_words[0]
    debug_print(f'First word: {first_word}')
    first_word_b = first_word.encode('utf-8')
    debug_print(f'First word as bytes: {first_word_b}')    


    plaintext_b = PLAINTEXT.encode('utf-8')
    key = pad(first_word_b, AES.block_size)
    cipher = AES.new(key, AES.MODE_CBC)
    ct_bytes = cipher.encrypt(pad(plaintext_b, AES.block_size))
    iv = b64encode(cipher.iv).decode('utf-8')
    ct = b64encode(ct_bytes).decode('utf-8')
    result = json.dumps({'iv':iv, 'ciphertext':ct})
    print(result)



if __name__ == "__main__":
    main()