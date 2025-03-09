import argparse
from transaction_processor import TransactionProcessor
from session import Session
from bank_account import BankAccount

# Formats a transaction for fixed 40-character length
def format_transaction(code, name, account, amount, misc=""):
    return f"{code.ljust(2)}_{name.ljust(20)}_{str(account).zfill(5)}_{str(amount).zfill(8)}_{misc.ljust(2)}"

# Formats account details for fixed 37-character length
def format_account(account: BankAccount):
    return f"{str(account.accountNumber).zfill(5)}_{account.accountName.ljust(20)}_{account.status}_{str(account.balance).zfill(8)}_{account.plan}"

def find_account(account_number, accounts):
    return next((acc for acc in accounts if acc.accountNumber == account_number), None)

def find_account_by_name(account_name, accounts):
    return next((acc for acc in accounts if acc.accountName == account_name), None)

def get_valid_number_input(prompt, min_value=None, max_value=None):
    while True:
        try:
            value = float(input(prompt))
            if min_value is not None and value < min_value:
                print(f"Error: Value must be at least {min_value}.")
                continue
            if max_value is not None and value > max_value:
                print(f"Error: Value cannot exceed {max_value}.")
                continue
            return value
        except ValueError:
            print("Error: Invalid input. Please enter a numeric value.")

def main():
    parser = argparse.ArgumentParser(description="Bank ATM command-line program.")
    parser.add_argument("transactions_file", nargs="?", default="transactions.txt", help="Path to bank account transaction file")
    parser.add_argument("accounts_file", nargs="?", default="accounts.txt", help="Path to current bank accounts file")
    parser.add_argument("log_file", nargs="?", default="log.txt", help="Path to log file")
    args = parser.parse_args()
    
    session = None
    transaction_processor = TransactionProcessor()
    transactions = []
    # Simulated existing accounts - change this when implementing the back end
    accounts = [
        BankAccount("23456", "Jane Doe", 500.00, adminPriv=False, status="A", plan="NP"),
        BankAccount("10002", "Bob Smith", 750.50, adminPriv=True, status="A", plan="SP"),
        BankAccount("10003", "Charlie Lee", 200.00, adminPriv=False, status="D", plan="NP")
    ]  
    log_output = []
    
    def log(message):
        print(message)
        log_output.append(message)
    
    log("Welcome to Bank ATM CLI. Enter commands (login, deposit, withdraw, transfer, paybill, create, delete, disable, changeplan, logout, exit):")
    while True:
        command = input("Enter command: ").strip().lower()
        
        if command == "login":
            if session:
                log("Error: Already logged in. Please logout first.")
                continue
            while True:
                session_type = input("Enter session type (standard/admin): ").strip().lower()
                if session_type in ["standard", "admin"]:
                    break
                log("Error: Invalid session type. Please enter 'standard' or 'admin'.")
            
            if session_type == "standard":
                while True:
                    name = input("Enter account holder's name: ").strip()
                    account = find_account_by_name(name, accounts)
                    if not account:
                        log("Error: Account holder name not found.")
                        continue
                    break
                session = Session(False, account)
            else:
                # Creating a temporary "admin account" to store admin privileges
                admin_account = BankAccount("00000", "Admin", 0.00, adminPriv=True, status="A", plan="NP")
                session = Session(True, admin_account)  # Associate session with the admin account

            log(f"Logged in as {session_type}.")

        elif command == "logout":
            if not session:
                log("Error: No active session to logout from.")
                continue
            transactions.append("00_END_OF_SESSION_______00000_00000000__")
            log("Transaction log:")
            with open(args.transactions_file, "w") as trans_file:
                for t in transactions:
                    log(t)
                    trans_file.write(t + "\n")
            with open(args.accounts_file, "w") as acc_file:
                for acc in accounts:
                    acc_file.write(format_account(acc) + "\n")
            with open(args.log_file, "w") as log_file:
                for entry in log_output:
                    log_file.write(entry + "\n")
            session = None
            log("Logged out successfully.")
        
        elif command in ["withdraw", "deposit", "transfer", "paybill"]:
            if not session:
                log("Error: Please login first.")
                continue
            account = session.currentAccount
            if not account:
                log("Error: No account associated with session.")
                continue
            if command == "withdraw":
                amount = get_valid_number_input("Enter withdrawal amount: ", min_value=0, max_value=500)
                while amount > account.balance:
                    log("Error: Insufficient funds.")
                    amount = get_valid_number_input("Enter withdrawal amount: ", min_value=0, max_value=500)
                account.balance -= amount
            elif command == "deposit":
                amount = get_valid_number_input("Enter deposit amount: ", min_value=0)
                account.balance += amount
            elif command == "transfer":
                to_account_number = input("Enter recipient account number: ").strip()
                to_account = find_account(to_account_number, accounts)
                if not to_account:
                    log("Error: Destination account does not exist.")
                    continue
                amount = get_valid_number_input("Enter transfer amount: ", min_value=0, max_value=1000)
                while amount > account.balance:
                    log("Error: Insufficient funds.")
                    amount = get_valid_number_input("Enter transfer amount: ", min_value=0, max_value=1000)
                account.balance -= amount
                to_account.balance += amount
            elif command == "paybill":
                while True:
                    company = input("Enter company (EC, CQ, FI): ").strip()
                    if company not in ["EC", "CQ", "FI"]:
                        log("Error: Invalid company selection.")
                        continue
                    break
                amount = get_valid_number_input("Enter bill amount: ", min_value=0, max_value=2000)
                while amount > account.balance:
                    log("Error: Insufficient funds.")
                    amount = get_valid_number_input("Enter bill amount: ", min_value=0, max_value=2000)
                account.balance -= amount
            log(f"{command.capitalize()} completed.")
        
        elif command in ["create", "delete", "disable", "changeplan"]:
            if not session or not session.currentAccount or not session.currentAccount.adminPriv:
                log("Error: Only admins can perform this action.")
                continue
            log(f"Executing {command}...")
            if command == "create":
                name = input("Enter new account holder name: ").strip()
                if len(name) > 20:
                    log("Error: Account holder name must be at most 20 characters.")
                    continue
                
                account_number = str(len(accounts) + 10000)  # Simple unique ID generation
                initial_balance = get_valid_number_input("Enter initial balance: ", min_value=0, max_value=999999.99)
                
                new_account = BankAccount(account_number, name, initial_balance, adminPriv=False, status="A", plan="NP")
                accounts.append(new_account)
                log("Account created successfully.")
                
            elif command == "delete":
                name = input("Enter account holder's name: ").strip()
                account = find_account_by_name(name, accounts)
                if not account:
                    log("Error: Account not found.")
                    continue
                accounts.remove(account)
                log("Account deleted successfully.")
                
            elif command == "disable":
                name = input("Enter account holder's name: ").strip()
                account = find_account_by_name(name, accounts)
                if not account:
                    log("Error: Account not found.")
                    continue
                account.status = "D"
                log("Account disabled successfully.")
                
            elif command == "changeplan":
                name = input("Enter account holder's name: ").strip()
                account = find_account_by_name(name, accounts)
                if not account:
                    log("Error: Account not found.")
                    continue
                account.plan = "SP" if account.plan == "NP" else "NP"
                log("Account payment plan updated successfully.")

        # Update the login process to correctly set admin privileges
        elif command == "login":
            if session:
                log("Error: Already logged in. Please logout first.")
                continue
            while True:
                session_type = input("Enter session type (standard/admin): ").strip().lower()
                if session_type in ["standard", "admin"]:
                    break
                log("Error: Invalid session type. Please enter 'standard' or 'admin'.")
            if session_type == "standard":
                while True:
                    name = input("Enter account holder's name: ").strip()
                    account = find_account_by_name(name, accounts)
                    if not account:
                        log("Error: Account holder name not found.")
                        continue
                    break
                session = Session(False, account)
            else:
                name = input("Enter admin account holder's name: ").strip()
                account = find_account_by_name(name, accounts)
                if not account or not account.adminPriv:
                    log("Error: No admin privileges for this account.")
                    continue
                session = Session(True, account)
            log(f"Logged in as {session_type}.")
            
        elif command == "exit":
            log("Exiting...")
            break
        else:
            log("Invalid command.")
    
if __name__ == "__main__":
    main()