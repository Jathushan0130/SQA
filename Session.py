class Session:
    def __init__(self, adminPriv: bool, currentAccount: BankAccount):
        self.adminPriv = adminPriv  # A boolean that returns true if the account has admin privileges
        self.currentAccount = currentAccount  # Holds a reference to the logged-in BankAccount
        self.transactions = []  # List of transactions in this session

    def login(self, adminPriv: bool, currentAccount: BankAccount):
        """Logs in a user with a session type and optional bank account."""
        self.adminPriv = adminPriv
        self.currentAccount = currentAccount if adminPriv == False else None

    def logout(self):
        """Logs out the current user and clears transactions."""
        self.adminPriv = False
        self.currentAccount = None
        self.transactions = []

    def addTransaction(self, transaction: TransactionDM):
        """Adds a transaction to the session's history."""
        self.transactions.append(transaction)

    def __str__(self):
        return f"Session({self.adminPriv}, Account: {self.currentAccount}, Transactions: {len(self.transactions)})"
