#!/usr/bin/env python3
# Programming Project OTP
# Sun Nov 19 2023
# Zack Chand
import argparse
import segno
from PIL import Image
import pyotp
import time
import base64
import secrets
#Generate a random base 32 secret
def generate_secret_base32():
    length=20
    # Generate secure random bytes
    random_bytes = secrets.token_bytes(length)
    # Encode these bytes into Base32
    base32_secret = base64.b32encode(random_bytes).decode('utf-8')
    # Remove any '=' padding as it's not required in TOTP
    return base32_secret.rstrip('=')
# Function to get OTP
def getOTP():
    # Loop that keeps generating OTP's every 30 seconds
    try:
        while True:
            #Generate Random Secret Key
            secret = generate_secret_base32()
            # Use pyotp's library to generate OTP's
            otp = pyotp.TOTP(secret)
            # Print the OTP values to the console
            print_otp = otp.now()
            print("Generated OTP: " , print_otp)
            # Sleep for 30 seconds 
            time.sleep(30)
    # When the use hits CTRL + C the program will exit
    except KeyboardInterrupt:
        print("Exiting Program ...")

# Function to make QR Code
#https://realpython.com/python-generate-qr-code/
def makeQr():

   # example from https://github.com/google/google-authenticator/wiki/Key-Uri-Format
    otpauth = 'otpauth://totp/ACME%20Co:john.doe@email.com?secret=HXDMVJECJJWSRB3HWIZR4IFUGFTMXBOZ&issuer=ACME%20Co&algorithm=SHA1&digits=6&period=30'
    generate_qr = segno.make_qr(otpauth)
    # Save the QR code with the scale of 10 x 10 pixels 
    generate_qr.save("qrcode.png" , scale = 10)
    # Open the image after it has been saved
    get_image = Image.open("qrcode.png")
    # Show the image after it is opened
    get_image.show()
    print(get_image.format)
# Main function
def main():
    # Argument Parser 
    parser = argparse.ArgumentParser(description="OTP Example")
    parser.add_argument('--generate-qr', action='store_true', help='Generate a QR code')
    parser.add_argument('--get-otp', action='store_true', help='Get an OTP')

    args = parser.parse_args()
    # Generata QR
    if args.generate_qr:
        print('Generating QR Code...')
        makeQr()
    #Get OTP
    elif args.get_otp:
        print('Getting OTP...')
        getOTP()
    # Throw an Error message if the user enters an invalid argument 
    else:
        print('No valid argument provided, please re-run the application with --generate-qr or --get-otp')
# Define main function
if __name__ == "__main__":
    main()
