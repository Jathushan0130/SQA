class TransactionProcessor:
      def deposit(self, session: Session, accounts: list, accountNumber: str, transactionAmnt: float) -> bool:
            account = self.getAccount(accounts, accountNumber)
            if account: 
                  account.balance += transactionAmnt
                  session.addTransaction(Transaction("deposit", accountNumber, transactionAmnt))
                  return True
            return False
      
      def withdraw(self, session: Session, accounts: list, accountNumber: str, transactionAmnt: float) -> bool:
            """Withdraw money from an account."""
            account = self.getAccount(accounts, accountNumber)
            if session.adminPriv == False and transactionAmnt > 500:
                  return False  # Withdrawal limit for standard users
            if account and (account.balance - transactionAmnt) >= 0:
                  account.balance -= transactionAmnt
                  session.addTransaction(Transaction("withdrawal", accountNumber, transactionAmnt))
                  return True
            return False

      def transfer(self, session: Session, accounts: list, fromAcc: str, toAcc: str, amount: float) -> bool:
            """Transfer money between two accounts."""
            sender = self.getAccount(accounts, fromAcc)
            receiver = self.getAccount(accounts, toAcc)
            if sender and receiver and amount <= 1000 and sender.balance >= amount:
                  sender.balance -= amount
                  receiver.balance += amount
                  session.addTransaction(Transaction("transfer", fromAcc, amount, toAcc))
                  return True
            return False

      def getAccount(self, accounts: list, accountNumber: str):
            """Finds an account by account number."""
            for acc in accounts:
                  if acc.accountNumber == accountNumber:
                        return acc
            return None
