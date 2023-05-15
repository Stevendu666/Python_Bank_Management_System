class Account:
    def __init__(self, customer_id, first_name, last_name, account_num, password, account_type, balance,
                 account_number_saving=None, account_number_checking=None,
                 balance_checking=0, balance_saving=0, credit_limit=None, iban_num=None):
        self.customer_id = customer_id
        self.first_name = first_name
        self.last_name = last_name
        self.account_num = account_num
        self.account_number_saving = account_number_saving
        self.account_number_checking = account_number_checking
        self.password = password
        self.account_type = account_type
        self.balance = balance
        self.balance_checking = balance_checking
        self.balance_saving = balance_saving
        self.credit_limit = credit_limit
        self.iban_num = iban_num
        self.last_transaction_date = None
        self.transaction_count = 0

    def __str__(self):
        return f"Account Number: {self.account_num}\nIBAN Number: {self.iban_num}\nAccount Type: {self.account_type}"


class SavingsAccount(Account):
    def __init__(self, account_num, iban_num, balance_saving, account_number_saving):
        super().__init__(None, None, None, account_num, None, "Savings Account", balance_saving,
                         balance_saving=balance_saving, account_number_saving=account_number_saving,
                         iban_num=iban_num)
        self.last_withdrawal_date = None
        self.last_transfer_date = None

    def __str__(self):
        return super().__str__() + f"\nSaving account number: {self.account_number_saving}"


class CheckingAccount(Account):
    def __init__(self, account_num, iban_num, credit_limit):
        super().__init__(None, None, None, account_num, None, "Checking Account", 0, balance_checking=0,
                         iban_num=iban_num, credit_limit=credit_limit)

    def __str__(self):
        return super().__str__() + f"\nCredit Limit: {self.credit_limit}"