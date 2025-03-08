import argparse
import sys
from transaction_processor import TransactionProcessor
from session import Session
from bank_account import BankAccount

# Formats a transaction for fixed 40-character length
def format_transaction(code, name, account, amount, misc=""):
    return f"{code.ljust(2)}_{name.ljust(20)}_{str(account).zfill(5)}_{str(amount).zfill(8)}_{misc.ljust(2)}"

# Formats account details for fixed 37-character length
def format_account(account: BankAccount):
    return f"{str(account.accountNumber).zfill(5)}_{account.accountName.ljust(20)}_{account.status}_{str(account.balance).zfill(8)}"

def main():
    parser = argparse.ArgumentParser(description="Bank ATM command-line program.")
    parser.add_argument("transactions_file", help="Path to bank account transaction file")
    parser.add_argument("accounts_file", help="Path to current bank accounts file")
    parser.add_argument("log_file", help="Path to log file")
    args = parser.parse_args()
    
    session = None
    transaction_processor = TransactionProcessor()
    transactions = []
    accounts = []  # Simulated in-memory accounts
    
    # Redirect console output to log file
    sys.stdout = open(args.log_file, "w")
    
    print("Welcome to Bank ATM CLI. Enter commands (login, deposit, withdraw, transfer, paybill, create, delete, disable, changeplan, logout, exit):")
    while True:
        command = input("Enter command: ").strip().lower()
        
        if command == "login":
            session_type = input("Enter session type (standard/admin): ").strip().lower()
            if session_type == "standard":
                name = input("Enter account holder's name: ").strip()
                session = Session(False, None)
                session.name = name
            elif session_type == "admin":
                session = Session(True, None)
            else:
                print("Invalid session type.")
                continue
            print(f"Logged in as {session_type}.")

        elif command in ["deposit", "withdraw", "transfer", "paybill"] and session:
            name = input("Enter account holder's name: ").strip() if session.adminPriv else session.name
            account_number = input("Enter account number: ").strip()
            amount = float(input("Enter amount: "))
            
            if command == "deposit":
                transactions.append(format_transaction("04", name, account_number, amount))
            elif command == "withdraw":
                transactions.append(format_transaction("01", name, account_number, amount))
            elif command == "transfer":
                to_account = input("Enter recipient account number: ").strip()
                transactions.append(format_transaction("02", name, account_number, amount, to_account))
            elif command == "paybill":
                company = input("Enter company (EC/CQ/FI): ").strip()
                if company in ["EC", "CQ", "FI"]:
                    transactions.append(format_transaction("03", name, account_number, amount, company))
                else:
                    print("Invalid company.")
                    continue
            print(f"{command.capitalize()} recorded.")

        elif command in ["create", "delete", "disable", "changeplan"] and session and session.adminPriv:
            name = input("Enter account holder's name: ").strip()
            account_number = input("Enter account number: ").strip()
            if command == "create":
                initial_balance = float(input("Enter initial balance: "))
                transactions.append(format_transaction("05", name, account_number, initial_balance))
                accounts.append(BankAccount(account_number, name, initial_balance))
            elif command == "delete":
                transactions.append(format_transaction("06", name, account_number, "00000000"))
            elif command == "disable":
                transactions.append(format_transaction("07", name, account_number, "00000000"))
            elif command == "changeplan":
                transactions.append(format_transaction("08", name, account_number, "00000000"))
            print(f"{command.capitalize()} recorded.")
        
        elif command == "logout" and session:
            transactions.append("00_END_OF_SESSION_______00000_00000000__")
            print("Transaction log:")
            with open(args.transactions_file, "w") as trans_file:
                for t in transactions:
                    print(t)
                    trans_file.write(t + "\n")
            with open(args.accounts_file, "w") as acc_file:
                for acc in accounts:
                    acc_file.write(format_account(acc) + "\n")
            session = None
            print("Logged out successfully.")
        
        elif command == "exit":
            print("Exiting...")
            break
        else:
            print("Invalid command or not logged in.")
    
    # Restore console output
    sys.stdout.close()
    sys.stdout = sys.__stdout__

if __name__ == "__main__":
    main()
