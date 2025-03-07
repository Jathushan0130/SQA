import argparse
import sys
from file_manager import FileManager
from transaction_processor import TransactionProcessor
from session import Session

def format_transaction(code, name, account, amount, misc=""):
    """Formats a transaction line to meet the 40-character requirement."""
    return f"{code.ljust(2)}_{name.ljust(20)}_{str(account).zfill(5)}_{str(amount).zfill(8)}_{misc.ljust(2)}"

def main():
    parser = argparse.ArgumentParser(description="Bank ATM command-line program.")
    parser.add_argument("accounts_file", help="Path to the current bank accounts file")
    parser.add_argument("transactions_file", help="Path to the transaction output file")
    args = parser.parse_args()

    file_manager = FileManager()
    accounts = file_manager.readAccountsFile(args.accounts_file)
    session = None
    transaction_processor = TransactionProcessor()
    transactions = []
    
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
            elif command == "delete":
                transactions.append(format_transaction("06", name, account_number, "00000000"))
            elif command == "disable":
                transactions.append(format_transaction("07", name, account_number, "00000000"))
            elif command == "changeplan":
                transactions.append(format_transaction("08", name, account_number, "00000000"))
            print(f"{command.capitalize()} recorded.")
        
        elif command == "logout" and session:
            transactions.append("00_END_OF_SESSION_______00000_00000000__")
            file_manager.writeTransactionsFile(args.transactions_file, transactions)
            session = None
            print("Logged out successfully.")
        
        elif command == "exit":
            print("Exiting without saving...")
            break
        else:
            print("Invalid command or not logged in.")

if __name__ == "__main__":
    main()