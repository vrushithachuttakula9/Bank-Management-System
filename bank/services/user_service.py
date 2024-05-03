from random import randint
from bank.services.validations import *
from bank.services.mailOperations import *
from bank.services.config import *
from bank.database.db_operations import *
from bank.services.user_security import *
import string
import time

class createAccount:
    def accountCreation(self):
        self.fname = input("Enter your first name:")
        self.lname = input("Enter your last name:")
        self.name = self.fname + self.lname
        self.gender = genderValidation()
        self.dob = dobValidation()
        self.mobileNo = mobileNoValidation()
        self.aadhar = input("Enter your 12 digit Aadhar number:")
        self.email = emailValidation()
        self.salt,self.password = passwordValidation()
        self.initialDeposit = float(input("Enter initial deposit:"))

        print()
        print("Otp verification process initiated..")
        print()

        if mailOtpVerification(senderMail, self.email):
            print("Otp verified Successfully")
            print()
            while 1:
                current_time = int(time.time() * 1000)  # Get the current timestamp in milliseconds
                random_part = randint(10000, 99999)
                self.accountNumber = int(f"{current_time}{random_part}")
                print("Account created successfully. Your account number is" + str(self.accountNumber))
                print()
                break

        insertData('users', first_name=self.fname, last_name=self.lname, email=self.email, dob=self.dob, salt=self.salt, password=self.password)

        self.userId = fetchData('users', email=self.email)

        insertData('accounts', user_id=self.userId[0][0], account_number=self.accountNumber, balance=self.initialDeposit, is_active=True)
        return

def login(user_mail):
    while True:
        if user_mail in fetchColumnData('users','email'):
            user_password = input("Password:")
            print()

            user_data = fetchData('users', email=user_mail)
            failedLoginAttempts = user_data[0][7]
            db_salt = user_data[0][5]
            db_password = user_data[0][6]

            if failedLoginAttempts > MAX_LOGIN_ATTEMPTS:
                print("Maximum Login Attempts exceeded.. Account Locked")
                print()
                return False
            else:
                hashed_user_password = hashedPassword(db_salt, user_password)

                if hashed_user_password == db_password:
                    updateData('users', values={'failedcountattempts': 0}, conditions={'email': user_mail})

                    last_login_date = user_data[0][8]
                    print("Last login date and time is "+str(last_login_date))

                    update_last_login(user_mail)
                    print("Login Successful..please select an option from below menu..")
                    print()
                    return True
                else:
                    failedLoginAttempts += 1
                    updateData('users', values={'failedcountattempts': failedLoginAttempts}, conditions={'email': user_mail})
                    return False

        else:
            print("Invalid email id, please try again..")
            return False
def forgotPassword():

    # taking user_mail id as input
    user_mail = input("Enter Mail Id: ")
    try:

        # fetching user data row from flm_users table based on user_mail
        db_data = fetchData('users', email=user_mail)

        # extracting user dob from user data row fetched
        db_dob = db_data[0][4]

        # taking dob from user for further validation
        user_dob = dobValidation()

        # checking database_dob with user_dob entered
        if user_dob == str(db_dob):

            # verifying again with OTP to change password
            if mailOtpVerification(senderMail,user_mail):

                # allowing user again to create new password
                updated_salt,updated_password = passwordValidation()

                # updating new password, salt into user database in flm_users table based on user_mail
                updateData('users', values={'password': updated_password,'salt': updated_salt}, conditions={'email': user_mail})

                return True
            else:
                print("[-] OTP Verification failed, Please try again...")
                return False
        else:
            print("[-] DOB Verification failed, Please try again...")
            return False

    except:
        return False

                        







