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


    # # if parameterCount == 3 and sys.argv[1] == "-p" and sys.argv[2].isnumber():
    # if param_count == 3 and sys.argv[1] == "-p" and sys.argv[2].isdigit():    # Changed from line above, 9/28/23, SAW
    #     key = int(sys.argv[2])
    #     printKeyMap(key)
    # elif param_count == 4 and sys.argv[2].isdigit():
    #     key = int(sys.argv[2])
    #     if sys.argv[1] == "-e":
    #         encrypt(key, sys.argv[3])
    #     elif sys.argv[1] == "-d":
    #         decrypt(key, sys.argv[3])
    #     else:
    #         printCliSyntax()
    # elif len(sys.argv) == 2 and sys.argv[1] == "-u":
    #     unitTests()
    # else:
    #     printCliSyntax()


if __name__ == "__main__":
    main()
