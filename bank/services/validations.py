import re
from datetime import datetime
import os
import hashlib
from random import randint
from bank.database.db_operations import *

def genderValidation():
    while True:
        gender = input("Enter your gender[m/f/o]:")
        regex = "(?:m|f|o)$"
        p = re.compile(regex)

        if re.search(p, gender):
            return True
        else:
            print("Invalid gender, please enter valid gender")
            print()

def dobValidation():
    while True:
        dob_input = input("Enter your date of birth in the format DD/MM/YYYY:")

        try:
            dob = datetime.strptime(dob_input, "%d/%m/%Y")
            return dob.strftime("%d/%m/%Y")  # Return the formatted valid date
        except ValueError:
            print("Invalid date of birth. Please use the format DD/MM/YYYY.")

def mobileNoValidation():
    while True:
        mobileNo = input("Enter your 10-digit mobile number: ")

        pattern = re.compile(r'^\d{10}$')
        if pattern.match(mobileNo):
            print("Valid mobile number.")
            return True
        else:
            print("Invalid mobile number. Please enter a 10-digit mobile number.\n")
def uniqueEmail(email):
    if email in fetchColumnData('users','email'):
        return False
    else:
        return True

def emailValidation():
    while True:
        emailId = input("Enter your email ID: ")

        pattern = re.compile(r'^[\w.-]+@[\w.-]+\.\w+$')  # Compile the regex pattern

        if uniqueEmail(emailId):

            if pattern.match(emailId):  # Use re.match to check if the input matches the pattern
                return emailId
            else:
                print("Enter a valid email address: ")
        else:
            print("Already registered with this email address")
            print()
            continue


def passwordValidation():
    while True:
            password = input("Enter your password: ")
            confirm_password = input("Re-enter your password: ")
            salt = randint(00000,99999)

            if password == confirm_password:
                password = str(salt)+password
                password = hashlib.sha256(password.encode()).hexdigest()
                return salt, password
            else:
                print("Password and confirm password do not match")
                print()
                continue
