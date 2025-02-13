import re 
import random

# validates name for valid input cases 
def validate_name(name):
    if len(name) > 20:
        return "Error: Name should be less than 20 characters."

    if re.search(r'\d', name):
        return "Error: Name should not contain numbers."

    if re.search(r'[^a-zA-Z\s]', name):
        return "Error: Name should not contain special characters."

    return True 

def standard_transaction(transaction):
	restricted_transactions = ["create", "delete", "disable", "change plan"]
	if transaction.lower() in restricted_transactions:
 		return "Error: Privileged transaction denied for standard user."

    	return "Transaction approved." #if user inputs unprivileged transactions such as deposit, withdrawal etc 

def admin_transaction(transaction):
	allowed_transaction = ["create", "delete", "disable", "change plan"]
 	if transaction.lower() in allowed_transaction:
  		return "Transaction approved for admin user"

# this function displays the bank account file different from bank account transactions file 
def display_bank_account(account_name, account_number, status, amount_of_funds):
	print(f"{account_number}_{account_name}_{status}_{amount_of_funds}")
	

def login():
	print("Hello, welcome to the banking system")

	session_type = input("Enter session type (standard/admin): ")

	if session_type == "standard":
		account_name = input("Please provide the account holder's name: ")
		if validate_name(account_name):
          		print("Login successful as Standard user.")
	    		display_bank_account(account_name)
       			transaction = input("Give a transaction to input: ")
       			standard_transaction(transaction)
	    	else:
      			print("Invalid input for user input")
	 
	elif session_type == "admin":
		account_name = input("Please provide the account holder's name: ")
		print("Login successful as Admin user")
  		display_bank_account(account_name)
           	transaction = input("Give a transaction to input: ")
    		admin_transaction(transaction)
  		
	else: 
		print("Invalid session type. Please select either 'standard' or 'admin'.")
		

def withdrawl(account_holder_name, account_number, amount, session_type):
    withdrawal = Withdrawal(account_holder_name, account_number, amount, session_type)
    return withdrawal.process_withdrawal()

def Deposit(account_name, account_number, amount_deposit):
	print("Deposit transaction selected")
	

def create():
    if(session == "standard"):
        print("this functions is unavliable to you ")
    else:
        print("please enter the name of the account")
        name = input()
        if len(name) > 20:
            print("the name you entered is too long (the max is 20 charaters)")
        else:
            name_number = str(random.randrange(1,99999))
            with open('test.txt') as file:
                contents = file.read()
                search_word = name_number
                if search_word in contents:
                    name_number = random.randrange(1,99999)
            print('your account number is: ' + name_number)
            print("how much money do you want to deposit with cents")
            amount = input()
            if float(amount) > 99999.99:
                print(amount + 'is larger the the max for creating a new acount ($99999.99)')
            file = open("test.txt", "a")
            file.write(name)
            file.write(': ')
            file.write(name_number)
            file.write(" $")
            file.write(amount)
            file.close()
            logout()

def changePlan():
    if(session == "standard"):
        print("this functions is unavliable to you ")
    else:
        print('please enter the name of the account you want to change the plan of')
        with open('test.txt') as file:
                contents = file.read()
                search_word = input()
                if search_word in contents:
                    print('enter the account number')
                    number = input()
                    with open('test.txt') as file:
                        contents = file.read()
                        search_word = number
                        if int(search_word) in contents:
                            print('would you like to change this student account to a non-student account')
                            decision = input()
                            if decision == 'yes':
                                print('the account is now a non-student')
                        else:
                            print('number given is not asscoiated with the name')
                else:
                    print('name not found in system')

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
