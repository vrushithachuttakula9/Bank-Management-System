from bank.database.db_operations import *

def fetch_userId(user_mail):
    user_data = fetchData('users', email=user_mail)

    try:
        userId = user_data[0][0]
        return userId

    except:
        return False

def displayBalance(user_mail):
    userId = fetch_userId(user_mail)

    if userId:
        accounts_data = fetchData('accounts', user_id=userId)
        print("Account Balance: " + str(accounts_data[0][3]))
        print()
        return True
    else:
        return False

def depositMoney(user_mail, depositAmount):
    userId = fetch_userId(user_mail)

    if userId:
        try:
            accounts_data = fetchData('accounts', user_id=userId)

            balance = accounts_data[0][3] + depositAmount

            updateData('accounts', values={'balance': balance}, conditions={'user_id': userId})
            displayBalance(user_mail)

            return True
        except mysql.connector.Error as e:
            print("Error", e)
            return False
    else:
        return False

def withdrawalMoney(user_mail, withdrawAmount):
    userId = fetch_userId(user_mail)

    if userId:
        accounts_data = fetchData('accounts', user_id=userId)

        balance = accounts_data[0][3]
        if balance > withdrawAmount:

            balance = balance - withdrawAmount

            updateData('accounts', values={"balance": balance}, conditions={'user_id': userId})
            displayBalance(user_mail)

            return True
        else:
            print("Insufficient funds")
            print()
            return False
    else:
        return False

def transferMoney(user_mail, transferAmount):
    senderUserId = fetch_userId(user_mail)

    senderDetails = fetchData('accounts', user_id=senderUserId)

    senderBalance = senderDetails[0][3]
    senderAccountId = senderDetails[0][0]
    senderAccountNumber = senderDetails[0][2]

    if senderBalance > transferAmount:

        receiverAccountId = int(input("Enter receipents account id:"))

        if receiverAccountId in fetchColumnData('accounts','account_id'):
            updatedSenderBalance = senderBalance - transferAmount

            updateData('accounts', values={'balance': updatedSenderBalance}, conditions={'user_id': senderUserId})
            displayBalance(user_mail)

            receiver_data = fetchData('accounts', account_id=receiverAccountId)
            receiverUserId = receiver_data[0][1]
            receiverAccountNumber = receiver_data[0][2]
            receiverBalance = receiver_data[0][3] + transferAmount

            updateData('accounts', values={'balance': receiverBalance}, conditions={'account_id': receiverAccountId})

            insertData('transactions', user_id=senderUserId, account_id=senderAccountId, amount=transferAmount, from_account=senderAccountNumber,
                        to_account=receiverAccountNumber, trans_type='db')

            insertData('transactions', user_id=receiverUserId, account_id=receiverAccountId, amount=transferAmount,
                        from_account=senderAccountNumber, to_account=receiverAccountNumber, trans_type='cd')

            return True
        else:
            print("Receiver Account do not exist")
            print()
            return False

    else:
        print("Insufficient Balance")
        print()
        return False

def transactionHistory(user_mail):
    try:
        conn = db_connection()
        cursor = conn.cursor()

        query = """
                    SELECT users.first_name, users.last_name, accounts.account_number, transactions.amount, transactions.from_account, transactions.to_account, transactions.trans_date, transactions.trans_type
                    FROM users
                    INNER JOIN transactions ON users.user_id = transactions.user_id
                    INNER JOIN accounts ON transactions.account_id = accounts.account_id
                    WHERE users.email = %s
                """

    # Execute the query with the provided user_email
        cursor.execute(query, (user_mail,))

        # Fetch and print the transaction history
        print("Transaction History for User:", user_mail)
        print("{:<15} {:<15} {:<20} {:<15} {:<15} {:<15} {:<15} {:<10}".format("First Name", "Last Name",
                                                                               "Account Number", "Amount",
                                                                               "From Account", "To Account", "Date",
                                                                               "Trans Type"))
        for row in cursor.fetchall():
            first_name, last_name, account_number, amount, from_account, to_account, trans_date, trans_type = row
            print(
                "{:<15} {:<15} {:<20} {:<12} {:<20} {:<20} {:<15} {:<10}".format(first_name, last_name, account_number,
                                                                                 amount, from_account, to_account,
                                                                                 str(trans_date),
                                                                                 trans_type))

        print()
        # Close the cursor and the database connection
        cursor.close()
        conn.close()

        return True


    except mysql.connector.Error as e:
        return False
