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
"""
import sys


DEBUG = True


def main():
    param_count = len(sys.argv)

    print(f'Num params: {param_count}') if DEBUG else 0
    print(f'sys.argv[0]: {sys.argv[0]}') if DEBUG else 0

    if param_count >= 2:
        print(f'sys.argv[1]: {sys.argv[1]}') if DEBUG else 0
        print(f'sys.argv[2]: {sys.argv[2]}') if DEBUG else 0


if __name__ == "__main__":
    main()
