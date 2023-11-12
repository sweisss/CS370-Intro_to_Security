"""
Seth Weiss
weissse@oregonstate.edu
CS 370 - Intro to Security
Fall 2023
Programming Project 3  - OTP

Description:
./submission --generate-qr : This command should generate a jpg picture
or svg picture of the QR code that encodes the URI GA expects. URI contains
secret keys along with the user id required for the TOTP algorithm.

Refer to the following link which provides details about the format of URI
and how to add extra information in URI.
https://github.com/google/google-authenticator/wiki/Key-Uri-Format

[65pts]./submission --get-otp : This command should generate an OTP which must
match the OTP generated by the Google Authenticator for that 30 second period
and print it to the screen. Optionally, you can make the program run such that it
prints the OTP and then sleeps for 30 seconds and then again prints another OTP
and keeps on going forever.
"""
import sys


def print_usage():
    print("""Usage: otp [OPTION...]
          
    --generate-qr            generate a QR code that encodes what the URI GA expects
          
    --get-otp                generate an OTP which matches the OTP generated by the 
                                Google Authenticator for that 30 second period and
                                prints it to the screen
          
    -h, --help               give this help list""")


def generate_qr():
    print('gonna generate that QR code!')


def get_otp():
    print('gotta get that otp!')


def main():
    usage_options = {
    '--generate-qr': generate_qr,
    '--get-otp': get_otp,
    '-h': print_usage,
    '--help': print_usage
    }
    
    if len(sys.argv) != 2:
        print_usage()

    else:
        flag = sys.argv[1]
        option = usage_options.get(flag, print_usage)
        option()


if __name__ == "__main__":
    main()
