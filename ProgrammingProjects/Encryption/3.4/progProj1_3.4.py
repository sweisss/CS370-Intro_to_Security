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
https://www.tutorialspoint.com/How-can-I-fill-out-a-Python-string-with-spaces
"""
import sys

# from Crypto.Cipher import AES
# from Crypto.Random import get_random_bytes

import json
from base64 import b64encode, b64decode
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes

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
IV_STR = "0" * 32
IV_HEX = bytearray.fromhex(IV_STR)
MAX_KEY_LEN = 15
DEBUG = False

debug_print = lambda input: print(input) if DEBUG else 0


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


    debug_print(f'AES.block_size: {AES.block_size}')
    debug_print(f'IV_STR: {IV_STR}')
    debug_print(f'IV_HEX: {IV_HEX}')

    plaintext_b = PLAINTEXT.encode('utf-8')

    # # key = pad(first_word_b, AES.block_size)
    # key = first_word_b.ljust(AES.block_size, b' ')
    # debug_print(f'Padded Key: {key}')
    # cipher = AES.new(key, AES.MODE_CBC, iv=IV_HEX)
    # ct_bytes = cipher.encrypt(pad(plaintext_b, AES.block_size))
    # debug_print(f'ct_bytes: {ct_bytes}')
    # ct = b64encode(ct_bytes).decode('utf-8')

    # ct_check = "3eCtzTutooJpNSNiqqDO2ZXiIiTMkbLofDVv2E/ZChk="

    # debug_print(f"ciphertext check: {ct == ct_check}")

    # cipher2 = AES.new(key, AES.MODE_CBC, IV_HEX)
    # pt = unpad(cipher2.decrypt(ct_bytes), AES.block_size)
    # debug_print(f'pt: {pt}')


    for word in small_words:
        word_bytes = word.encode('utf-8')
        key = word_bytes.ljust(AES.block_size, b' ')
        cipher = AES.new(key, AES.MODE_CBC, IV_HEX)
        ct_bytes = cipher.encrypt(pad(plaintext_b, AES.block_size))
        ct = b64encode(ct_bytes).decode('utf-8')

        if ct_bytes == CIPHER_HEX:
            print('Found a match')
            print(f'Known Ciphertext: {CIPHER_STR}')
            print(f'Calculated Ciphertext: {ct}')

            cipher2 = AES.new(key, AES.MODE_CBC, IV_HEX)
            plaintext2 = unpad(cipher2.decrypt(ct_bytes), AES.block_size)
            print(f'Known plaintext: {PLAINTEXT}')
            print(f'Calculated plaintext: {plaintext2.decode()}')

            print(f'Keyword: {word}')


if __name__ == "__main__":
    main()
