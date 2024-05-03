from bank.services.config import *
from bank.services.user_service import *

senderMail = admin_mail
password = App_pass
#
# def generate_otp():
#     x = ''.join(random.choices(string.digits, k=6))  # Generates a 6-digit OTP
#     return x
#
#
# def mailOtpVerification(senderMail, email):
#
#     server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
#     server.login(senderMail, password)
#     otp = generate_otp()
#     print(otp)
#     message = "Your OTP number is :" + otp  # Create the message with the generated OTP
#     server.sendmail(senderMail, email, message)
#
#     server.quit()
#     print()
#     print("Email sent successfully.")

import os
import math
import random
import smtplib

digits = "0123456789"
OTP = ""

for i in range(6):      
    OTP += digits[math.floor(random.random() * 10)]

otp = OTP + " is your OTP"
message = otp

def mailOtpVerification(senderMail, email):
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()


    s.login(senderMail, password)
    s.sendmail('&&&&&&', email, message)

    a = input("Enter your OTP >>: ")
    if a == OTP:
        print("Verified")
        return True
    else:
        print("Please Check your OTP again")
        return False



