class Logout:
    def __init__(self, session_active):
        self.session_active = session_active
        self.transaction_file = "daily_transaction_file.txt"

    def process_logout(self):
        """Handles user logout and session termination."""
        if not self.session_active:
            return "No active session. Please log in first."
        
        print("Logging out...")
        self.session_active = False  # Intentional issue: Doesn't properly clear session data
        
        with open(self.transaction_file, "a") as file:
            file.write("Transaction: Logout\n")
            file.write("Session ended.\n")
        
        print("Logout complete.")
        return "User logged out."