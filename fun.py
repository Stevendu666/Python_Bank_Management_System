import csv
import random
from cl import *
import datetime

####################   Login   ####################

def login():
    # Get user input for customer ID and password
    account_num = input("Enter account num: ")
    password = input("Enter Password: ")

    # Read customer information from CSV file
    with open('customer.csv', mode='r') as file:
        reader = csv.reader(file)
        # Skip header row
        next(reader)
        # Find row with matching account number and validate password
        for row in reader:
            if row[7] == account_num and row[8] == password:
                # Create a dictionary with customer information
                customer_info = {
                    'Customer ID': row[0],
                    'First Name': row[1],
                    'Last Name': row[2],
                    'Age': row[3],
                    'Phone': row[4],
                    'Address': row[5],
                    'Email': row[6],
                    'Account Number': row[7],
                    'Password': row[8],
                    'Account Type': row[9],
                    'IBAN Number': row[10]
                }
                # Display customer information
                print("\nCustomer Information:")
                for key, value in customer_info.items():
                    print(f"{key}: {value}")
                return

    # If account number or password is incorrect, display an error message
    print("\nInvalid account number or password.")


# Test the login function
# login()



####################   Create Account   ####################

def create_account():
    # Load customer information from file
    with open('customer.csv', mode='r') as file:
        reader = csv.reader(file)
        rows = [row for row in reader]

    # Prompt for customer information
    print("You are going to create a new customer account, Please follow the instruction, please enter the customer information:")
    first_name = input("First Name: ")
    last_name = input("Last Name: ")
    address = input("Address: ")
    phone = input("Phone number: ")
    age = input("Age: ")
    email = input("Email: ")
    password = input("Please set a 6-digit password for your account: ")
    while len(password) != 6 or not password.isdigit():
        password = input("Invalid password format. Please set a 6-digit password: ")
    confirm_password = input("Please confirm your password: ")
    while confirm_password != password:
        confirm_password = input("Password does not match. Please confirm your password again: ")

    # Check if customer already exists
    for row in rows:
        if first_name == row[1] and last_name == row[2] and age == row[3]:
            print("This customer already exists. Please go to login page to access your account.")
            # login()
            return

    # Load customer information from file
    with open('customer.csv', mode='r') as file:
        reader = csv.reader(file)
        rows = [row for row in reader]

    # Generate unique account and IBAN numbers
    existing_account_nums = [row[7] for row in rows]
    existing_iban_nums = [row[10] for row in rows]

    while True:
        account_num = str(random.randint(10000000, 99999999))
        iban_num = "IE" + str(random.randint(10 ** 20, 10 ** 21 - 1))

        if account_num not in existing_account_nums and iban_num not in existing_iban_nums:
            break

    # Display success message and account number
    print(f"\nCongratulations! Your account has been created successfully. Your account number is {account_num}.")

    # Create account type based on age
    customer_id = str(len(rows)).zfill(6)
    account_types = []
    credit_limits = 0
    account_num_checking = []
    account_num_saving = []
    if int(age) >= 18:
        print("\nPlease select the account type(s):")
        print("1. Savings Account")
        print("2. Checking Account")
        account_type_choices = input("Enter your choices separated by comma (e.g. 1,2): ")

        # Create account based on selected type
        for choice in account_type_choices.split(','):
            if choice == "1":
                print("\nCreating Savings Account...")
                account_num_saving = "S" + account_num
                account_types.append("SavingsAccount")
                print(
                    f"\nCongratulations! Your saving account has been created successfully. "
                    f"Your saving account number is {account_num_saving}. "
                    f"The saving account only allows you to withdraw or transfer money once a month.")
            elif choice == "2":
                print("\nCreating Checking Account...")
                account_num_checking = "C" + account_num
                credit_limit = 500
                account_types.append("CheckingAccount")
                print(
                    f"\nCongratulations! Your checking account has been created successfully. "
                    f"Your checking account number is {account_num_checking}. "
                    f"The checking account credit limit is {credit_limit}.")
            else:
                print(f"\nInvalid input {choice}. Please try again.")
                return

    elif int(age) >= 14:
        print("\nYou cannot create checking account. Creating Savings Account for Teenager...")
        account_num_saving = "S" + account_num
        account_types.append("Teenager")
        print(
            f"\nCongratulations! Your saving account has been created successfully. "
            f"Your saving account number is {account_num_saving}. "
            f"The saving account only allows you to withdraw or transfer money once a month.")

    else:
        print("\nYou are not old enough to open an account.")
        return

    # Add new customer record to rows list
    new_row = [
        customer_id,
        first_name,
        last_name,
        age,
        phone,
        address,
        email,
        account_num,
        password,
        "|".join(account_types),
        iban_num
    ]
    rows.append(new_row)

    # Write rows list to file
    with open('customer.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(rows)
        print("New customer record added successfully!")

    # Add new account record to account.csv
    account_rows = []
    with open('account.csv', mode='r') as file:
        reader = csv.reader(file)
        for row in reader:
            account_rows.append(row)
    new_account_row = [
        customer_id,
        first_name,
        last_name,
        account_num,
        password,
        "|".join(account_types),
        "0.0",  # balance for main account
        account_num_checking,
        "0.0",  # balance for checking account
        credit_limits,
        account_num_saving,
        "0.0",  # balance for savings account
        iban_num
    ]
    account_rows.append(new_account_row)
    with open('account.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(account_rows)


####################   Modify Account   ####################


def modify_account():
    # Load customer information from file
    with open('customer.csv', mode='r') as file:
        reader = csv.reader(file)
        rows = [row for row in reader]

    # Prompt for account number
    account_number = input("Please enter your account number: ")
    customer_found = False
    for row in rows:
        if row[7] == account_number:
            customer_found = True
            break

    if not customer_found:
        print("Customer not found. Please try again.")
        return

    # Prompt for account number
    password = input("Please enter your password: ")
    password_found = False
    for row in rows:
        if row[8] == password:
            password_found = True
            break

    if not password_found:
        print("Password is not correct. Please try again.")
        return

    # Prompt for modification options
    print(f"\nPlease select the information to modify for account {account_number}:")
    print("1. Password")
    print("2. Phone Number")
    print("3. Address")
    print("4. Email")
    print("5. Name or Age")
    print("6. Delete Account")
    modification_choice = input("Enter your choice (1-5): ")

    # Modify customer information based on selected option
    if modification_choice == "1":
        new_password = input("Please enter your new password: ")
        while len(new_password) != 6 or not new_password.isdigit():
            new_password = input("Invalid password format. Please enter a 6-digit password: ")
        row[7] = new_password
        print("Password updated successfully!")
    elif modification_choice == "2":
        new_phone = input("Please enter your new phone number: ")
        row[4] = new_phone
        print("Phone number updated successfully!")
    elif modification_choice == "3":
        new_address = input("Please enter your new address: ")
        row[5] = new_address
        print("Address updated successfully!")
    elif modification_choice == "4":
        email = input("Please enter your new Email address: ")
        row[6] = email
        print("Address updated successfully!")
    elif modification_choice == "5":
        print("Name and age couldn't modify in this system, please go to the bank counter")
    elif modification_choice == "6":
        rows.remove(row)
        print("Account deleted successfully!")
    else:
        print(f"\nInvalid input {modification_choice}. Please try again.")
        return

    # Write updated rows list to file
    with open('customer.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(rows)


####################   View account information   ####################

def view_account():
    # Read CSV file
    with open('account.csv', mode='r') as file:
        reader = csv.reader(file)
        # Skip header row
        next(reader)
        # Iterate over each account row
        for row in reader:
            # Create a dictionary with account information
            account_info = {
                'Customer ID': row[0],
                'First Name': row[1],
                'Last Name': row[2],
                'Account Number': row[3],
                'Account Type': row[5],
                'Balance': float(row[6]),
                'Checking Account Number': row[7],
                'Checking Balance': float(row[8]),
                'Credit Limit': int(row[9]) if row[9] != '[]' else None,
                'Saving Account Number': row[10],
                'Saving Balance': float(row[11]),
                'IBAN Number': row[12]
            }
            # Display account information
            print("\nAccount Information:")
            for key, value in account_info.items():
                print(f"{key}: {value}")


# Example usage
# account_num = "12345678"
# password = "password"
# view_account(account_num, password)


####################   Account operation   ####################

def account_operations():
    # Read CSV file

    with open('account.csv', mode='r') as file:
        reader = csv.reader(file)
        # Skip header row
        next(reader)
        # Find row with matching customer ID
        # for row in reader:
        #     account_types = [tp for tp in row[5].split("|")]
        #     break
        # else:
            # account_types = []

        # account_type = account_types[0]
        # print(f"You have a {account_type} account. You can operate this account by now.")

        while True:
            choice = input("Please choose an account type (1. Checking / 2. Savings): ")
            if choice == "1":
                checking_account_operations()
                break
            elif choice == "2":
                savings_account_operations()
                # checking_account_operations()
                break
            else:
                print("Invalid choice. Please try again.")





####################   Checking Account Operations   ####################

def get_current_time():
    import datetime
    # Get the current timestamp in the desired format
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

import uuid

def generate_transaction_id():
    # 使用 UUID 来生成唯一的交易ID
    transaction_id = str(uuid.uuid4())
    return transaction_id


def checking_account_operations():
    # Read account information from CSV file
    with open('account.csv', mode='r') as file:
        reader = csv.reader(file)

        # Check if the file is empty
        try:
            # Skip header row
            next(reader)
        except StopIteration:
            print("No account information found.")
            return

        # Find row with matching account number
        for row in reader:
            # Update customer object with account information
            customer_id = row[0]
            first_name = row[1]
            last_name = row[2]
            account_number_checking = row[7]
            balance_checking = float(row[8])
            account_number_saving = row[10]
            balance_saving = float(row[11])
            credit_limit = int(row[9]) if row[9] != '[]' else None

    while True:
        print("""
        Checking Account Operations:
        1. View Balance
        2. Deposit
        3. Withdraw
        4. Transfer
        5. Back
        """)
        choice = input("Please enter your choice (1/2/3/4/5): ")

        transaction_limit = 0

        if choice == "1":
            # View checking Balance

            print(f"Current checking Balance: {balance_checking}")

        elif choice == "2":

            # Deposit

            amount = float(input("Please enter the amount to deposit: "))

            balance_checking += amount

            print(f"${amount} deposited successfully.")

            balance = balance_checking + balance_saving

            print(f"Current total balance: {balance}")

            # Update account.csv with the new balance

            update_account_balance(account_number_checking, balance_checking)

            # Record transaction

            transaction = {

                'transaction_id': generate_transaction_id(),

                'customer_id': customer_id,

                'first_name': first_name,

                'last_name': last_name,

                'transaction_time': get_current_time(),

                'sender_account': account_number_checking,

                'receiver_account': account_number_checking,

                'amount': amount,

                'transaction_type': 'Deposit',

                'balance': balance

            }

            record_transaction(transaction)

        elif choice == "3":
            # Withdraw

            amount = float(input("Please enter the amount to withdraw: "))
            withdraw_checking(customer_id, amount)

        elif choice == "4":
            # Transfer
            print("Note that you will be transferring funds from your current checking account to another")
            # sender_account = input("Please enter your account number (Checking account): ")
            # receiver_account = input("Please enter the recipient account number (Checking account/Saving account): ")
            # amount = float(input("Please enter the amount to transfer: "))
            transfer()
            # recipient_account_num = input("Please enter the recipient account number(Saving account/Checking account): ")
            break
        elif choice == "5":
            # Back
            break

        else:
            print("Invalid choice. Please try again.")


def update_account_balance(account_number, new_balance):
    # Read account.csv file and update the balance
    rows = []
    with open('account.csv', mode='r') as file:
        reader = csv.reader(file)
        rows = list(reader)
        for row in rows:
            if row[7] == account_number:
                row[8] = str(new_balance)
                balance = row[8] + row[11]
                row[6] = balance
            elif row[10] == account_number:
                row[11] = str(new_balance)
                balance = row[8] + row[11]
                row[6] = balance
                break  # Stop searching after finding the matching account

    # Write the updated rows back to the account.csv file
    with open('account.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(rows)

    return balance

def record_transaction(transaction):
    # Write the transaction to the transaction.csv file
    with open('transaction.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([
            transaction['transaction_id'],
            transaction['customer_id'],
            transaction['first_name'],
            transaction['last_name'],
            transaction['transaction_time'],
            transaction['sender_account'],
            transaction['receiver_account'],
            transaction['amount'],
            transaction['transaction_type'],
            transaction['balance']
        ])

####################   Transfer   ####################




def transfer():
    # Read account.csv file
    sender_account = input("Please enter your account number (Checking account): ")
    receiver_account = input("Please enter the recipient account number (Checking account/Saving account): ")
    amount = float(input("Please enter the amount to transfer: "))

    if amount <= 0:
        print("Invalid transfer amount. Please enter a positive number.")
        return

    # Read account information from CSV file
    with open('account.csv', mode='r') as file:
        reader = csv.reader(file)
        rows = list(reader)

        for row in rows:
            customer_id = row[0]
            first_name = row[1]
            last_name = row[2]
            if sender_account == row[7]:
                sender_balance_checking = float(row[8])
                if sender_balance_checking < amount:
                    print("Insufficient balance for transfer.")
                    return
                sender_balance_checking -= amount
                # Update sender's checking balance in account.csv
                update_account_balance(sender_account, sender_balance_checking)
            if receiver_account == row[7]:
                receiver_balance_checking = float(row[8])
                receiver_balance_checking += amount
                # Update receiver's checking balance in account.csv
                update_account_balance(receiver_account, receiver_balance_checking)
            elif receiver_account == row[10]:
                receiver_balance_saving = float(row[11])
                receiver_balance_saving += amount
                # Update receiver's saving balance in account.csv
                update_account_balance(receiver_account, receiver_balance_saving)

    # Record the transaction
    transaction_id = generate_transaction_id()
    transaction_time = get_current_time()

    sender_transaction = {
        'transaction_id': transaction_id,
        'customer_id': customer_id,
        'first_name': first_name,
        'last_name': last_name,
        'transaction_time': transaction_time,
        'sender_account': sender_account,
        'receiver_account': receiver_account,
        'amount': amount,
        'transaction_type': 'Transfer Sent',
        'balance': sender_balance_checking
    }
    receiver_transaction = {
        'transaction_id': transaction_id,
        'customer_id': customer_id,
        'first_name': first_name,
        'last_name': last_name,
        'transaction_time': transaction_time,
        'sender_account': sender_account,
        'receiver_account': receiver_account,
        'amount': amount,
        'transaction_type': 'Transfer Received',
        'balance': receiver_balance_checking
    }

    # Record the transactions in transaction.csv
    record_transaction(sender_transaction)
    record_transaction(receiver_transaction)

    print(f"${amount} transferred successfully from {sender_account} to {receiver_account}.")
    print(f"Sender's current checking balance: {sender_balance_checking}")





####################   Withdraw   ####################

def withdraw_checking(customer_id, amount):
    # Read account.csv file
    rows = []
    with open('account.csv', mode='r') as file:
        reader = csv.reader(file)
        rows = list(reader)
        for row in rows:
            if row[0] == customer_id:
                balance_checking = float(row[8])
                account_number_checking = row[7]
                credit_limit = int(row[9]) if row[9] != '[]' else None

                # Check if the balance is sufficient for withdrawal
                if balance_checking >= amount or (credit_limit is not None and balance_checking - amount >= -credit_limit):
                    balance_checking -= amount

                    # Update account.csv with the new balances
                    balance = update_account_balance(account_number_checking, balance_checking)
                    # Record the transaction
                    transaction_id = generate_transaction_id()
                    transaction = {
                        'transaction_id': transaction_id,
                        'customer_id': customer_id,
                        'first_name': row[1],
                        'last_name': row[2],
                        'transaction_time': get_current_time(),
                        'sender_account': account_number_checking,
                        'receiver_account': account_number_checking,
                        'amount': amount,
                        'transaction_type': 'Withdrawal',
                        'balance': balance
                    }
                    record_transaction(transaction)

                    print(f"${amount} withdrawn successfully.")
                    print(f"Current total balance: {balance}")
                else:
                    print("Insufficient balance for withdrawal.")
                break  # Stop searching after finding the matching customer

def withdraw_saving(customer_id, amount):
    # Read account.csv file
    rows = []
    with open('account.csv', mode='r') as file:
        reader = csv.reader(file)
        rows = list(reader)
        for row in rows:
            if row[0] == customer_id:
                balance_saving = float(row[11])
                account_number_saving = row[10]

                # Check if the balance is sufficient for withdrawal
                if balance_saving >= amount:
                    balance_saving -= amount

                    balance = update_account_balance(account_number_saving, balance_saving)  # Update account.csv with the new balances


                    # Record the transaction
                    transaction_id = generate_transaction_id()
                    transaction = {
                        'transaction_id': transaction_id,
                        'customer_id': customer_id,
                        'first_name': row[1],
                        'last_name': row[2],
                        'transaction_time': get_current_time(),
                        'sender_account': account_number_saving,
                        'receiver_account': account_number_saving,
                        'amount': amount,
                        'transaction_type': 'Withdrawal',
                        'balance': balance

                    }
                    record_transaction(transaction)

                    print(f"${amount} withdrawn successfully.")
                    print(f"Current total balance: {balance}")
                else:
                    print("Insufficient balance for withdrawal.")
                break  # Stop searching after finding the matching customer


####################   View transaction history   ####################

def view_transaction_records():
    # Read transaction records from CSV file
    transactions = []
    with open('transaction.csv', mode='r') as file:
        reader = csv.DictReader(file)
        transactions = list(reader)

    # Print the transaction records
    if len(transactions) > 0:
        print("Transaction Records:")
        for transaction in transactions:
            print("---------------------------")
            print("---------------------------")
            for field, value in transaction.items():
                print(f"{field}: {value}")
    else:
        print("No transaction records found.")

# view_transaction_records()
# checking_account_operations()



####################   Savings Account Operations   ####################
#
def savings_account_operations():
    # Read account information from CSV file
    with open('account.csv', mode='r') as file:
        reader = csv.reader(file)
        # Skip header row
        next(reader)
        # Find row with matching account number
        for row in reader:
            # Update customer object with account information
            customer_id = row[0]
            first_name = row[1]
            last_name = row[2]
            account_number_checking = row[7]
            balance_checking = float(row[8])
            account_number_saving = row[10]
            balance_saving = float(row[11])
            credit_limit = int(row[9]) if row[9] != '[]' else None

    while True:
        print("""
          Checking Account Operations:
          1. View Balance
          2. Deposit
          3. Withdraw
          4. Transfer
          5. Back
          """)
        choice = input("Please enter your choice (1/2/3/4/5): ")

        transaction_limit = 0

        if choice == "1":
            # View checking Balance

            print(f"Current checking Balance: {balance_saving}")

        elif choice == "2":

            # Deposit

            amount = float(input("Please enter the amount to deposit: "))

            balance_saving += amount

            print(f"${amount} deposited successfully.")

            balance = balance_checking + balance_saving

            print(f"Current total balance: {balance}")

            # Update account.csv with the new balance

            update_account_balance(account_number_saving, balance_saving)

            # Record transaction

            transaction = {

                'transaction_id': generate_transaction_id(),

                'customer_id': customer_id,

                'first_name': first_name,

                'last_name': last_name,

                'transaction_time': get_current_time(),

                'sender_account': account_number_saving,

                'receiver_account': account_number_saving,

                'amount': amount,

                'transaction_type': 'Deposit',

                'balance': balance

            }

            record_transaction(transaction)

        elif choice == "3":
            # Withdraw

            amount = float(input("Please enter the amount to withdraw: "))
            withdraw_saving(customer_id, amount)

        elif choice == "4":
            # Transfer
            print("Note that you will be transferring funds from your current checking account to another")
            # sender_account = input("Please enter your account number (Checking account): ")
            # receiver_account = input("Please enter the recipient account number (Checking account/Saving account): ")
            # amount = float(input("Please enter the amount to transfer: "))
            transfer()
            # recipient_account_num = input("Please enter the recipient account number(Saving account/Checking account): ")
            break
        elif choice == "5":
            # Back
            break

        else:
            print("Invalid choice. Please try again.")

        #     # Read account information from CSV file
        # with open('account.csv', mode='r') as file:
        #     reader = csv.reader(file)
        #
        #     # Check if the file is empty
        #     try:
        #         # Skip header row
        #         next(reader)
        #     except StopIteration:
        #         print("No account information found.")
        #         return
        #
        #     # Find row with matching account number
        #     for row in reader:
        #         # Update customer object with account information
        #         customer_id = row[0]
        #         first_name = row[1]
        #         last_name = row[2]
        #         account_number_checking = row[7]
        #         balance_checking = float(row[8])
        #         account_number_saving = row[10]
        #         balance_saving = float(row[11])
        #         credit_limit = int(row[9]) if row[9] != '[]' else None
        #
        # while True:
        #     print("""
        #        Checking Account Operations:
        #        1. View Balance
        #        2. Deposit
        #        3. Withdraw
        #        4. Transfer
        #        5. Back
        #        """)
        #     choice = input("Please enter your choice (1/2/3/4/5): ")
        #
        #     transaction_limit = 0
        #
        #     if choice == "1":
        #         # View checking Balance
        #
        #         print(f"Current checking Balance: {balance_checking}")
        #
        #     elif choice == "2":
        #
        #         # Deposit
        #
        #         amount = float(input("Please enter the amount to deposit: "))
        #
        #         balance_checking += amount
        #
        #         print(f"${amount} deposited successfully.")
        #
        #         balance = balance_checking + balance_saving
        #
        #         print(f"Current total balance: {balance}")
        #
        #         # Update account.csv with the new balance
        #
        #         update_account_balance(account_number_checking, balance_checking)
        #
        #         # Record transaction
        #
        #         transaction = {
        #
        #             'transaction_id': generate_transaction_id(),
        #
        #             'customer_id': customer_id,
        #
        #             'first_name': first_name,
        #
        #             'last_name': last_name,
        #
        #             'transaction_time': get_current_time(),
        #
        #             'sender_account': account_number_checking,
        #
        #             'receiver_account': account_number_checking,
        #
        #             'amount': amount,
        #
        #             'transaction_type': 'Deposit',
        #
        #             'balance': balance
        #
        #         }
        #
        #         record_transaction(transaction)
        #
        #     elif choice == "3":
        #         # Withdraw
        #
        #         amount = float(input("Please enter the amount to withdraw: "))
        #         withdraw_checking(customer_id, amount)

# checking_account_operations()








# def transfer(sender_account, receiver_account, amount):
#     # Read account information from CSV file
#     accounts = []
#     with open('account.csv', mode='r') as file:
#         reader = csv.DictReader(file)
#         accounts = list(reader)
#
#     sender = None
#     receiver = None
#
#     # Find sender and receiver accounts
#     for account in accounts:
#         if account['account_num'] == sender_account:
#             sender = account
#         if account['account_num'] == receiver_account:
#             receiver = account
#
#     # Check if sender and receiver accounts are found
#     if sender is None:
#         print("Sender account not found.")
#         return
#     if receiver is None:
#         print("Receiver account not found.")
#         return
#
#     sender_balance = float(sender['balance'])
#     receiver_balance = float(receiver['balance'])
#
#     # Check if the sender has sufficient balance for the transfer
#     if sender_balance < amount:
#         print("Insufficient balance for transfer.")
#         return
#
#     # Perform the transfer
#     sender_balance -= amount
#     receiver_balance += amount
#
#     # Update account balances
#     sender['balance'] = str(sender_balance)
#     receiver['balance'] = str(receiver_balance)
#
#     # Update account.csv file with the new balances
#     with open('account.csv', mode='w', newline='') as file:
#         writer = csv.DictWriter(file, fieldnames=accounts[0].keys())
#         writer.writeheader()
#         writer.writerows(accounts)
#
#     # Record the transaction in the transaction.csv file
#     transaction_id = generate_transaction_id()
#     transaction_time = get_current_time()
#     transaction = {
#         'customer_id': sender['customer_id'],
#         'first_name': sender['first_name'],
#         'last_name': sender['last_name'],
#         'transaction_id': transaction_id,
#         'transaction_time': transaction_time,
#         'sender_account': sender_account,
#         'receiver_account': receiver_account,
#         'amount': amount,
#         'transaction_type': 'Transfer',
#         'balance': sender_balance
#     }
#     record_transaction(transaction)
#
#     print(f"${amount} transferred successfully from {sender_account} to {receiver_account}.")
#     print(f"Sender's current balance: {sender_balance}")


# def update_account_balance_2(row, new_balance):
#     row[8] = str(new_balance)
#     # Update the account.csv file with the new balance
#     with open('account.csv', mode='w', newline='') as file:
#         writer = csv.writer(file)
#         writer.writerows(rows)

    # else:
    #     with open('account.csv', mode='r') as file:
    #         reader = csv.reader(file)
    #         rows = list(reader)
    #
    #         for row in rows:
    #             customer_id = row[0]
    #             if sender_account == row[7]:
    #                 sender_balance_checking = float(row[8])
    #                 sender_balance_checking -= amount
    #                 balance = update_account_balance(sender_account, sender_balance_checking)
    #             if receiver_account == row[7]:
    #                 receiver_balance_checking = float(row[8])
    #                 receiver_balance_checking += amount
    #             elif receiver_account == row[10]:
    #                 receiver_balance_saving = float(row[11])
    #                 receiver_balance_saving += amount
    #                 # Update account.csv with the new balances
    #                 balance = update_account_balance(receiver_account, receiver_balance_saving)
    #
    #
    #
    #
    #                     # Record the transaction
    #                     transaction_id = generate_transaction_id()
    #                     transaction = {
    #                         'transaction_id': transaction_id,
    #                         'customer_id': customer_id,
    #                         'first_name': row[1],
    #                         'last_name': row[2],
    #                         'transaction_time': get_current_time(),
    #                         'sender_account': sender_account,
    #                         'receiver_account': receiver_account,
    #                         'amount': amount,
    #                         'transaction_type': 'Withdrawal',
    #                         'balance': balance
    #                     }
    #                     record_transaction(transaction)
    #
    #                     print(f"${amount} withdrawn successfully.")
    #                     print(f"Current total balance: {balance}")
    #                 else:
    #                     print("Insufficient balance for withdrawal.")
    #                 break  # Stop searching after finding the matching customer
                # # Initialize variables
    # sender_info = {}
    # receiver_info = {}
    #
    # # Read account information from CSV file
    # try:
    #     with open('account.csv', mode='r') as file:
    #         reader = csv.reader(file)
    #         # Skip header row
    #         next(reader)
    #
    #         # Find sender and receiver account numbers
    #         for row in reader:
    #             if row[7] == sender_account:
    #                 sender_info = {
    #                     "customer_id": row[0],
    #                     "first_name": row[1],
    #                     "last_name": row[2],
    #                     "balance_checking": float(row[8]),
    #                     "balance_saving": float(row[11]),
    #                     "account": sender_account
    #                 }
    #             if row[7] == receiver_account or row[10] == receiver_account:
    #                 receiver_info = {
    #                     "customer_id": row[0],
    #                     "first_name": row[1],
    #                     "last_name": row[2],
    #                     "balance_checking": float(row[8]),
    #                     "balance_saving": float(row[11]),
    #                     "account": receiver_account
    #                 }
    # except Exception as e:
    #     print(f"An error occurred while reading the account file: {str(e)}")
    #     return
    #
    # # Check if the sender and receiver accounts are found
    # if not sender_info:
    #     print("Sender account not found.")
    #     return
    # elif not receiver_info:
    #     print("Receiver account not found.")
    #     return
    #
    # # Check if the sender has sufficient balance for the transfer
    # sender_total_balance = sender_info["balance_checking"] + sender_info["balance_saving"]
    # if sender_info["balance_checking"] >= amount:
    #     # Perform the transfer
    #     sender_info["balance_checking"] -= amount
    #     if receiver_info["account"] == row[7]:  # Checking account
    #         receiver_info["balance_checking"] += amount
    #     else:  # Saving account
    #         receiver_info["balance_saving"] += amount
    #
    #     # Update account balances in account.csv
    #     # update_account_balance(sender_account, sender_info["balance_checking"]+sender_info["balance_saving"])
    #     # update_account_balance(receiver_account, receiver_info["balance_checking"]+receiver_info["balance_saving"])
    #
    #     # Record the transactions
    #     transaction_id = generate_transaction_id()
    #     transaction_time = get_current_time()
    #
    #     sender_transaction = {
    #         'transaction_id': transaction_id,
    #         'customer_id': sender_info["customer_id"],
    #         'first_name': sender_info["first_name"],
    #         'last_name': sender_info["last_name"],
    #         'transaction_time': transaction_time,
    #         'sender_account': sender_account,
    #         'receiver_account': receiver_account,
    #         'amount': amount,
    #         'transaction_type': 'Transfer Sent',
    #         'balance': sender_info["balance_checking"]
    #     }
    #     receiver_transaction = {
    #         'transaction_id': transaction_id,
    #         'customer_id': receiver_info["customer_id"],
    #         'first_name': receiver_info["first_name"],
    #         'last_name': receiver_info["last_name"],
    #         'transaction_time': transaction_time,
    #         'sender_account': sender_account,
    #         'receiver_account': receiver_account,
    #         'amount': amount,
    #         'transaction_type': 'Transfer Received',
    #         'balance': receiver_info["balance_checking"] if receiver_info["account"] == row[7] else receiver_info[
    #             "balance_saving"]
    #     }
    #
    #     record_transaction(sender_transaction)
    #     record_transaction(receiver_transaction)
    #
    #     print(f"€{amount} transferred successfully from {sender_account} to {receiver_account}.")
    #     print(f"Sender's current total balance: {sender_info['balance_checking'] + sender_info['balance_saving']}")
    # else:
    #     print("Insufficient balance for transfer.")

        # def update_account_balance(account_num, new_balance):
#     # Read account.csv file
#     rows = []
#     with open('account.csv', mode='r') as file:
#         reader = csv.reader(file)
#         rows = list(reader)
#
#     # Update the balance in the rows list
#     for row in rows:
#         if row[7] == account_num:
#             row[8] = str(new_balance)
#
#     # Write the updated rows back to the account.csv file
#     with open('account.csv', mode='w', newline='') as file:
#         writer = csv.writer(file)
#         writer.writerows(rows)




# def transfer():
#     # Read account.csv file
#     sender_account = input("Please enter your account number (Checking account): ")
#     receiver_account = input("Please enter the recipient account number (Checking account/Saving account): ")
#     amount = float(input("Please enter the amount to transfer: "))
#
#     # Read account information from CSV file
#     with open('account.csv', mode='r') as file:
#         reader = csv.reader(file)
#         # Skip header row
#         next(reader)
#         # Find row with matching account number
#         for row in reader:
#             if row[7] == sender_account:
#                 sender_balance_checking = float(row[8])
#                 sender_balance_saving = float(row[11])
#                 break
#             if row[7] == receiver_account or row[10] == receiver_account:
#                 receiver_balance_checking = float(row[8])
#                 receiver_balance_saving = float(row[11])
#                 break
#
#         # Check if the sender has sufficient balance for the transfer
#         if sender_balance_checking >= amount:
#             # Perform the transfer
#             sender_balance_checking -= amount
#             receiver_balance_checking += amount
#
#         # # row[8] = str(balance_checking)
#         # account_number_checking = row[7]
#         # balance_saving = float(row[11])
#
#         balance = sender_balance_checking + sender_balance_saving
#         update_account_balance(balance_checking, balance)  # Update account.csv with the new balances
#
#         # Record the transaction
#         transaction_id = generate_transaction_id()
#         transaction = {
#             'transaction_id': transaction_id,
#             'customer_id': customer_id,
#             'first_name': row[1],
#             'last_name': row[2],
#             'transaction_time': get_current_time(),
#             'sender_account': account_number_checking,
#             'receiver_account': receiver_customer,
#             'amount': amount
#             'transaction_type': 'Withdrawal',
#             'balance': balance
#         }
#         record_transaction(transaction)
#
#
#         if sender_customer_id == "":
#             print("Sender account not found.")
#         elif receiver_customer_id == "":
#             print("Receiver account not found.")
#         else:
#             # Perform the transfer
#             # Implement the transfer logic here
#
#             print("Transfer completed successfully.")
#
#
# sender_customer_id = ""
#     receiver_customer_id = ""
#
#     with open('account.csv', mode='r') as file:
#         reader = csv.reader(file)
#         rows = list(reader)
#         for row in rows:
#             if row[7] == sender_account:
#                 balance_checking = float(row[8])
#
#
#
#     # Find sender and receiver account numbers
#     with open('account.csv', mode='r') as file:
#         reader = csv.reader(file)
#         next(reader)  # Skip header row
#         for row in reader:
#             if row[7] == sender_account:
#
#             if row[7] == receiver_account or row[10] == receiver_account:
#                 receiver_customer_id = row[0]
#
#     if sender_customer_id == "":
#         print("Sender account not found.")
#     elif receiver_customer_id == "":
#         print("Receiver account not found.")
#     else:
#         # Perform the transfer
#         # Implement the transfer logic here
#
#         print("Transfer completed successfully.")
#
#     with open('account.csv', mode='r') as file:
#         reader = csv.reader(file)
#         rows = list(reader)
#         sender_balance_checking = 0.0
#         receiver_balance_checking = 0.0
#         sender_balance_saving = 0.0
#         receiver_balance_saving = 0.0
#         for row in rows:
#             if row[0] == sender_customer_id:
#                 sender_balance_checking = float(row[8])
#                 sender_balance_saving = float(row[11])
#                 break
#         for row in rows:
#             if row[0] == receiver_customer_id:
#                 receiver_balance_checking = float(row[8])
#                 receiver_balance_saving = float(row[11])
#                 break
#
#                 # Check if the sender has sufficient balance for the transfer
#                 if sender_balance_checking >= amount:
#                     # Perform the transfer
#                     sender_balance_checking -= amount
#                     receiver_balance_checking += amount
#
#                     row[8] = str(balance_checking)
#                     account_number_checking = row[7]
#                     balance_saving = float(row[11])
#                     balance = balance_checking + balance_saving
#                     update_account_balance(balance_checking, rows)  # Update account.csv with the new balances
#
#                     # Record the transaction
#                     transaction_id = generate_transaction_id()
#                     transaction = {
#                         'transaction_id': transaction_id,
#                         'customer_id': customer_id,
#                         'first_name': row[1],
#                         'last_name': row[2],
#                         'transaction_time': get_current_time(),
#                         'sender_account': account_number_checking,
#                         'receiver_account': account_number_checking,
#                         'amount': amount,
#                         'transaction_type': 'Withdrawal',
#                         'balance': balance
#                     }
#                     record_transaction(transaction)
#
#
#             # Update the sender's and receiver's balances
#             update_account_balance(sender_account_num, sender_balance_checking,
#                                    sender_balance_saving)
#             update_account_balance(rows, receiver_customer_id, receiver_account_num, receiver_balance_checking,
#                                    receiver_balance_saving)
#
#             # Calculate the new total balance
#             sender_balance = sender_balance_checking + sender_balance_saving
#             receiver_balance = receiver_balance_checking + receiver_balance_saving
#
#             # Record the transaction
#             transaction_id = generate_transaction_id()
#             transaction_time = get_current_time()
#
#             sender_transaction = {
#                 'transaction_id': transaction_id,
#                 'customer_id': sender_customer_id,
#                 'first_name': '',
#                 'last_name': '',
#                 'transaction_time': transaction_time,
#                 'sender_account': sender_account_num,
#                 'receiver_account': receiver_account_num,
#                 'amount': amount,
#                 'transaction_type': 'Transfer Sent',
#                 'balance': sender_balance
#             }
#             receiver_transaction = {
#                 'transaction_id': transaction_id,
#                 'customer_id': receiver_customer_id,
#                 'first_name': '',
#                 'last_name': '',
#                 'transaction_time': transaction_time,
#                 'sender_account': sender_account_num,
#                 'receiver_account': receiver_account_num,
#                 'amount': amount,
#                 'transaction_type': 'Transfer Received',
#                 'balance': receiver_balance
#             }
#
#             record_transaction(sender_transaction)
#             record_transaction(receiver_transaction)
#
#             print(f"${amount} transferred successfully from {sender_account_num} to {receiver_account_num}.")
#             print(f"Sender's current total balance: {sender_balance}")
#         else:
#             print("Insufficient balance for transfer.")
