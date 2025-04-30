import mysql.connector
from decimal import Decimal
class Bank:
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
        self.conn =mysql.connector.connect(
            host="localhost",
            user="root",
            password="Welc$me@45",
            database="bank_system")
        self.cursor= self.conn.cursor()

    def user_validation(self):
        while self.attempts < 3:
            self.cursor.execute("SELECT * FROM users WHERE username = %s", (self.user,))
            user_data = self.cursor.fetchone()
            if user_data:
                print("Username validated.")
                self.pass_validation(user_data)
                return
            else:
                self.attempts += 1
                if self.attempts < 3:
                    self.user = input("Username not found. Try again (Attempt {} of 3): ".format(self.attempts + 1))
                else:
                    print("Try again later.")
                    self.cursor.close()
                    self.conn.close()
                    return

    def pass_validation(self,user_data):
        attempts = 0
        while attempts < 3:
            entered_pass = int(input("Enter your password: "))
            if entered_pass == user_data[2]: # here user_data[0] is id, [1] is username ,[2] is password and [3] is balance
                print("Password validated. Welcome to your bank account!")
                self.balance = user_data[3]
                self.bank_operations()
                return
            else:
                attempts += 1
                if attempts < 3:
                    print("Incorrect password. Try again.")
                else:
                    print("Try again later.")
                    self.cursor.close()
                    self.conn.close()
                    return

    def bank_operations(self):
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
            amount=Decimal(amount)
            self.balance += amount
            self.cursor.execute("UPDATE users SET balance =%s Where username= %s",(self.balance,self.user))
            self.conn.commit()
            print(f"${amount} deposited successfully. New balance: ${self.balance}")
        else:
            print("Deposit amount must be greater than zero.")

    def withdraw(self, amount):
        if amount <= self.balance:
            amount=Decimal(amount)
            self.balance -= amount
            self.cursor.execute("UPDATE users SET balance = %s WHERE username = %s", (self.balance, self.user))
            self.conn.commit()
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
