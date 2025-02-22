import tkinter as tk
from tkinter import messagebox

def create_account_window():
    window = tk.Tk()
    window.title("Create Account")

    tk.Label(window, text="Name").grid(row=0)
    tk.Label(window, text="Email").grid(row=1)
    tk.Label(window, text="Phone Number").grid(row=2)
    tk.Label(window, text="Password").grid(row=3)

    name_entry = tk.Entry(window)
    email_entry = tk.Entry(window)
    phone_entry = tk.Entry(window)
    password_entry = tk.Entry(window, show='*')

    name_entry.grid(row=0, column=1)
    email_entry.grid(row=1, column=1)
    phone_entry.grid(row=2, column=1)
    password_entry.grid(row=3, column=1)

    def register():
        name = name_entry.get()
        email = email_entry.get()
        phone = phone_entry.get()
        password = password_entry.get()
        if name and email and phone and password:
            register_user(name, email, phone, password)
            messagebox.showinfo("Success", "Account created successfully")
        else:
            messagebox.showerror("Error", "All fields are required")

    tk.Button(window, text="Register", command=register).grid(row=4, column=1)
    window.mainloop()
