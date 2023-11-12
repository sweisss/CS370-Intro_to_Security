# Project Overview
This program generates a QR code compatible with the Google Authenticator (GA) app
([Android](https://play.google.com/store/apps/details?id=com.google.android.apps.authenticator2&hl=en_US),
[iOS](https://apps.apple.com/us/app/google-authenticator/id388497605),
[Source](https://github.com/google/google-authenticator)). The QR code can be scanned into the GA and used to generate One Time Passwords (OTPs) for a 2nd factor authentication (2FA) method. 

# Setup Info
Download and unzip (if commpressed) the prject into your directory of choice. Create a venv and install requirements.txt. Please see the suggested commands below. 

To create [venv](https://docs.python.org/3/library/venv.html):
```
python -m venv /path/to/new/virtual/environment
```

To activate venv:

```
source venv/Scripts/activate
```

To activate WSLvenv:

```
source WSLvenv/bin/activate
```

To activate venv on Mac or flip:
```
source venv/bin/activate
```

To deactivate venv:

```
deactivate
```
#### Python version
WSL: 3.8.10

Mac: 3.10.10

## Set up the environment
Set up your venv using your preferred methods.
Once the venv is activated, navigate your venv shell to the project directory and install the necessary dependencies by running the following
command:
```
pip install -r requirements.txt
```

# Run the program
The progam takes one of two possible arguments: `--generate-qr` or `--get-otp`.

To run the program enter the following command, replacing <argument> with the argument of your choice.
```
python otp.py <argument>
```

## Generate a QR code
To generate a QR code, run the following command:
```
python otp.py --generate-qr
```
The default settings for this command will create a random base32 secret and save it in a file named
_.secrets_ in the project directory.
The program then uses this secret to generate a Google Authenitcator app commpatible URI using the
[PyOTP](https://pyauth.github.io/pyotp/) library. The URI is then used to generate a QR code with
the [qrcode](https://pypi.org/project/qrcode/) library. 

The default settings will save this QR code to a PNG file in the project directory, as well as print it
to the console. 

Use the Google Authenticator app on your mobile device to scan the QR code and add the profile.
Once scanned, the profile will automatically be saved in the app and generate a new OTP every 30 seconds. 

To modify the file type or location, see the [Modify the program](#modify-the-program) section below.

## Verify the OTP
To verify your OTP, run the following command:
```
python otp.py --get-otp
```
This will read the _.secrets_ file and generate a [TOPT](https://pyauth.github.io/pyotp/#time-based-otps)
(Time-Based OTP) using the PyOTP library. The program prints this TOTP to the console. 

Because it shares the same secret in the _.secrets_ file, the OTPs
will be synchronized with the ones being generated in the GA app.

Re-runing the `--get-otp` command will always display the most recent TOTP. 

> *NOTE:* if you generate a new QR code, it will overwrite the _.secrets_ file, and subsequent calls to 
> `--get-otp` will display the most recent OTP for the most recent secret.

## Modify the program
Open _otp.py_ in your favorite text editor. At the top of the program you will find the following constants:
```
SECRETS_FILE = '.secrets'
QR_PNG_FILENAME = 'qr_code.png'
QR_SVG_FILENAME = 'qr_code.svg'
USERNAME = 'Seth Weiss'
APP_NAME = 'Project 3 - OTP'
WRITE_QR_SVG = False
WRITE_QR_PNG = True
PRINT_QR_TO_CONSOLE = True
```
The first three constants can be modified to change the location where the files are saved. 

The `USERNAME` and `APP_NAME` constants will be displayed in the Google Authenticator app, and can be changed
appropriately. 

The last three constants control the output formats of the QR code. Select `True` or `False` as desired for each.
