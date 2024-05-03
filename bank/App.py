from bank.services.banking_service import *
from bank.services.user_service import *
from bank.services.banner_printing import *
# from bank.services.config import *
import time

# Entry banner printing
try:
    entryBannerPrinting()
except:
    print("Banner Loading Failed..")
    quit()

# choice table
while True:
    # Displaying Main Menu Options
    print("Main Menu Options:")
    print("1. Register")
    print("2. Login")
    print("3. Forgot Password")
    print("4. Exit")
    print()
    choice = input("Enter your choice: ")

    if choice == "1":
        # Account Registration
        print("Processing")
        time.sleep(2)

        # Calling a function to create a new account
        ca = createAccount()
        ca.accountCreation()
        continue

    elif choice == "2":
        # accessing existing account
        print()

        user_mail = input("Username(Email): ")

        # Login
        if login(user_mail) == False:
            print("Login Failed")
            print()
            continue
        else:
            while True:
                print("1. Display Balance")
                print("2. Deposit Money")
                print("3. Withdraw Money")
                print("4. Transfer Money")
                print("5. Transaction History")
                print("6. Logout")
                print()

                choice = input("Enter your choice: ")

                if choice == "1":
                    print()

                    # calling the function that displays balance
                    if displayBalance(user_mail):
                        pass
                    else:
                        print("Unable to display balance")
                        print()

                elif choice == "2":
                    print()

                    try:
                        depositAmount = int(input("Enter your deposit amount: "))
                        print()
                    except:
                        print("Enter valid amount..")
                        print()
                        continue

                    # calling function that is responsible to deposit money
                    if depositMoney(user_mail, depositAmount):
                        print("Money deposited successfully.")
                        print()
                    else:
                        print("Deposit Unsuccessful")
                        print()

                elif choice == "3":
                    print()

                    try:
                        withdrawAmount = int(input("Enter withdrawal amount: "))
                        print()
                    except:
                        print("Enter valid amount..")
                        print()

                    # calling the function that is responsible for money withdrawal
                    if withdrawalMoney(user_mail, withdrawAmount):
                        print("Withdrawal Successful..")
                        print()
                        continue

                    else:
                        print("Withdrawal Unsuccessful")
                        print()
                        continue

                elif choice == "4":
                    print()

                    try:
                        transferAmount = int(input("Enter amount to be transferred: "))
                    except:
                        print("Enter valid amount")
                        print()
                        continue

                     # calling the function that is responsible to transfer money
                    if transferMoney(user_mail, transferAmount):
                        print("Transfer successful..")
                        print()
                        continue
                    else:
                        print("Transfer Unsuccessful")
                        print()
                        continue

                elif choice == "5":
                    print()

                    # Function call that displays transaction history
                    if transactionHistory(user_mail):
                        continue
                    else:
                        print("Failed to get transaction history")
                        print()
                        continue

                elif choice == "6":
                    # Logout functionality
                    print("Logout successful")
                    print()
                    break



    elif choice == "3":
        # Forgot password
        if forgotPassword():
            print("Password Reset Successful")
            print()
            continue
        else:
            print("Password Reset Failed")
            print()
            continue


    elif choice == "4":
        #Exit App
        exitBannerPrinting()
        print()
        print("Thank you")
        quit()
