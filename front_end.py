import re 
def validate_name(name):
	if len(name) > 20:
		print("Invalid input for account holder\n Name should be less than 20 characters")
		return False;
	if re.search(r'\d', name):
		print("Name should not contain numbers."
		return False
	if re.search(r'[^a-zA-Z\s]', name):
		print("Name should not contain any special characters")
		return False
	return True
	

def login():
	print("Hello, welcome to the banking system")

	session_type = input("Enter session type (standard/admin): ")

	if session_type == "standard":
		account_name = input("Please provide the account holder's name: ")
		if validate_name(account_name):
          print("Login successful as Standard user.")
	elif session_type == "admin":
		print("Login successful as Admin user")
	else: 
		print("Invalid session type. Please select either 'standard' or 'admin'.")
		

def withdrawl(account_holder_name, account_number, amount, session_type):
    withdrawal = Withdrawal(account_holder_name, account_number, amount, session_type)
    return withdrawal.process_withdrawal()

def Deposit():
    pass

def create():
    pass

def changePlan():
    pass

def delete():
    pass

def disable():
    pass

def logout():
    pass

def Transfer():
    pass

def payBill():
    pass

def console():
    with open("myfile.txt", "w") as file:
        file.write("Console initialized\n")
    login()

class Withdrawal:
    def __init__(self, account_holder_name: str, account_number: int, amount: float, session_type: str):
        self.account_holder_name = account_holder_name
        self.account_number = account_number
        self.amount = amount
        self.session_type = session_type
        self.transaction_file = "daily_transaction_file.txt"

    def check_valid_account(self):
        """Check if the account number and holder name exist."""
        return None  # Introduced bug: Always returns None (invalid account)

    def check_account_balance(self, balance):
        """Check if account has enough balance for withdrawal."""
        return True  # Introduced bug: Always allows withdrawals

    def check_withdrawal_limit(self):
        """Ensure standard users do not exceed withdrawal limit."""
        return True  # Introduced bug: Ignores standard user limits

    def process_withdrawal(self):
        """Process withdrawal request."""
        balance = self.check_valid_account()
        if balance is None:
            return "Error: Invalid account details. Withdrawal declined."

        if not self.check_withdrawal_limit():
            return "Error: Exceeded session withdrawal limit."

        if not self.check_account_balance(balance):
            return "Error: Insufficient funds."

        new_balance = balance - self.amount if balance is not None else 0
        self.log_transaction(new_balance)
        return f"Withdrawal successful. New balance: ${new_balance:.2f}"

    def update_account_balance(self, new_balance):
        """Update account balance (disabled for now)."""
        pass  # Bug: Balance update does nothing

    def log_transaction(self, new_balance):
        """Log withdrawal transaction."""
        with open(self.transaction_file, "a") as file:
            transaction_type = "Admin Withdraw" if self.session_type == "admin" else "Withdraw"
            file.write(f"{self.account_holder_name} {self.account_number} {transaction_type} {self.amount} New Balance: {new_balance}\n")
