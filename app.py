# it is using sample data 
class Bank:
    # Database with username, password, and balance for each user
    db = {
        "user1": {"password": 1234, "balance": 5000},
        "user2": {"password": 345, "balance": 3000},
        "user3": {"password": 7849, "balance": 1000}
    }

    def __init__(self, user):
        self.user = user
        self.passw = None
        self.balance = None
        self.attempts = 0

    def user_validation(self):
        # User validation with a maximum of 3 attempts
        while self.attempts < 3:
            if Bank.db.get(self.user):
                print("Username validated.")
                self.pass_validation()
                return
            else:
                self.attempts += 1
                if self.attempts < 3:
                    self.user = input("Username not found. Try again (Attempt {} of 3): ".format(self.attempts + 1))
                else:
                    print("Try again later.")
                    return

    def pass_validation(self):
        # Password validation with a maximum of 3 attempts
        attempts = 0
        while attempts < 3:
            entered_pass = int(input("Enter your password: "))
            if Bank.db.get(self.user)["password"] == entered_pass:
                print("Password validated. Welcome to your bank account!")
                self.balance = Bank.db.get(self.user)["balance"]
                self.bank_operations()
                return
            else:
                attempts += 1
                if attempts < 3:
                    print("Incorrect password. Try again.")
                else:
                    print("Try again later.")
                    return

    def bank_operations(self):
        # Start deposit/withdraw operations after successful login
        while True:
            print(f"Your current balance: ${self.balance}")
            operation = input("Choose an operation - Deposit (D), Withdraw (W), Exit (E): ").upper()

            if operation == 'D':
                amount = float(input("Enter amount to deposit: "))
                self.deposit(amount)
            elif operation == 'W':
                amount = float(input("Enter amount to withdraw: "))
                self.withdraw(amount)
            elif operation == 'E':
                print("Thank you for using the ATM. Goodbye!")
                break
            else:
                print("Invalid operation. Please choose again.")

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            Bank.db[self.user]["balance"] = self.balance
            print(f"${amount} deposited successfully. New balance: ${self.balance}")
        else:
            print("Deposit amount must be greater than zero.")

    def withdraw(self, amount):
        if amount <= self.balance:
            self.balance -= amount
            Bank.db[self.user]["balance"] = self.balance
            print(f"${amount} withdrawn successfully. New balance: ${self.balance}")
        else:
            print(f"Insufficient funds. Your current balance is ${self.balance}. Cannot withdraw ${amount}.")

# Main program flow
print("Hello!! Welcome to the ATM")

# Input username and create Bank object for that username
username = input("Enter your Username: ")
bank_user = Bank(username)

# Validate user and password
bank_user.user_validation()
