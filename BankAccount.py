class BankAccount:
    def __init__(self, accountNumber: int, accountName: str, balance: float, status: str = 'A'):
        self.accountNumber = accountNumber
        self.accountName = accountName
        self.balance = balance
        self.status = status  # 'A' for active, 'D' for disabled
        self.transactions = []  # List to store transaction history

    def add_transaction(self, transaction):
        self.transactions.append(transaction)

    def __str__(self):
        return f"Account({self.accountNumber}, {self.accountName}, Balance: {self.balance}, Status: {self.status})"
        