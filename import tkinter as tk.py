import random
import pyttsx3
import tkinter as tk
from tkinter import messagebox, simpledialog
from twilio.rest import Client

# Initialize the text-to-speech engine
engine = pyttsx3.init()

# Twilio credentials (replace with your own credentials)
account_sid = '[replacw eith your id]'
auth_token = '[replace with your id]'
twilio_whatsapp_number = 'whatsapp:+14155*****6'

# Create a Twilio client
client = Client(account_sid, auth_token)

# Mock database for testing
users_db = {
    "user1": {"password": "pass1", "balance": 5000, "whatsapp": "whatsapp:+91**********"},
    "user2": {"password": "pass2", "balance": 10000, "whatsapp": "whatsapp:+91**********"}
}

def speak(text):
    engine.say(text)
    engine.runAndWait()

def generate_otp():
    return random.randint(1000, 9999)

def login(username, password):
    return users_db.get(username) if users_db.get(username, {}).get("password") == password else None

def check_balance(username):
    balance = users_db[username]["balance"]
    message = f"Your current balance is: {balance} rupees"
    client.messages.create(body=message, from_=twilio_whatsapp_number, to=users_db[username]["whatsapp"])
    return message

def withdraw(username, amount):
    if users_db[username]["balance"] >= amount:
        users_db[username]["balance"] -= amount
        message = f"Withdrawal successful. Remaining balance: {users_db[username]['balance']} rupees"
    else:
        message = "Insufficient funds"
    client.messages.create(body=message, from_=twilio_whatsapp_number, to=users_db[username]["whatsapp"])
    return message

def deposit(username, amount):
    users_db[username]["balance"] += amount
    message = f"Deposit successful. New balance: {users_db[username]['balance']} rupees"
    client.messages.create(body=message, from_=twilio_whatsapp_number, to=users_db[username]["whatsapp"])
    return message

# GUI-based login system
def submit_login():
    username = username_entry.get()
    password = password_entry.get()
    user = login(username, password)
    if user:
        otp = generate_otp()
        client.messages.create(body=f"Your OTP is: {otp}", from_=twilio_whatsapp_number, to=users_db[username]["whatsapp"])
        entered_otp = simpledialog.askinteger("OTP Verification", "Enter OTP sent to your WhatsApp:")
        if otp == entered_otp:
            messagebox.showinfo("Login Successful", "You have successfully logged in!")
            transaction_menu(username)
        else:
            messagebox.showerror("Error", "Invalid OTP. Access Denied.")
    else:
        messagebox.showerror("Error", "Invalid username or password.")

def transaction_menu(username):
    transaction_window = tk.Toplevel(tk_window)
    transaction_window.title("Banking System")
    tk.Label(transaction_window, text=f"Welcome, {username}").pack()
    
    def handle_transaction(choice):
        if choice == "1":
            messagebox.showinfo("Balance Inquiry", check_balance(username))
        elif choice == "2":
            amount = simpledialog.askinteger("Withdraw", "Enter amount to withdraw:")
            messagebox.showinfo("Withdrawal", withdraw(username, amount))
        elif choice == "3":
            amount = simpledialog.askinteger("Deposit", "Enter amount to deposit:")
            messagebox.showinfo("Deposit", deposit(username, amount))
        elif choice == "4":
            transaction_window.destroy()
    
    tk.Button(transaction_window, text="Check Balance", command=lambda: handle_transaction("1")).pack()
    tk.Button(transaction_window, text="Withdraw", command=lambda: handle_transaction("2")).pack()
    tk.Button(transaction_window, text="Deposit", command=lambda: handle_transaction("3")).pack()
    tk.Button(transaction_window, text="Exit", command=lambda: handle_transaction("4")).pack()

# Main window
tk_window = tk.Tk()
tk_window.title("Banking Login")
tk.Label(tk_window, text="Username").grid(row=0, column=0)
username_entry = tk.Entry(tk_window)
username_entry.grid(row=0, column=1)
tk.Label(tk_window, text="Password").grid(row=1, column=0)
password_entry = tk.Entry(tk_window, show="*")
password_entry.grid(row=1, column=1)
tk.Button(tk_window, text="Login", command=submit_login).grid(row=2, columnspan=2)
tk_window.mainloop()
