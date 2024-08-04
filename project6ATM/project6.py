#GUI
import tkinter as tk     #tkinter used to create GUI(display window)
from tkinter import messagebox    #to show a text pop up whenever a specific event occurs
from tkinter import ttk     #themed tkinter for more visual effects

#To store account details
import json   #javascript notation which locally stores data in a text file
import os     #to managefile path



#using imported json in this class below
#Note: In this code we can create multiple and access only one account at a time
class AccDetails:
    #store filename and load existing accounts
    def __init__(self, filename):
        self.filename = filename
        self.accounts = self.load_accounts()

    #for loading account data if exists and returns empty dictionary if not
    def load_accounts(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as file:
                return json.load(file)
        return {}

    #manages changes made in accounts
    def save_accounts(self):
        with open(self.filename, 'w') as file:
            json.dump(self.accounts, file)

    #manages login part for existing account
    def get_account(self, card_number):
        return self.accounts.get(card_number)

    #manages create account
    def create_account(self, card_number, password):
        if card_number in self.accounts:
            return False #if account already exists
        self.accounts[card_number] = {'password': password, 'balance': 0}
        self.save_accounts()
        return True   #if doesnt already exists

#created ATM class to handle details after successful login
class ATM:
    def __init__(self, card_number, password, balance=0):
        self.card_number = card_number
        self.password = password
        self.balance = balance

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            return True
        return False

    def withdraw(self, amount):
        if 0 < amount <= self.balance:
            self.balance -= amount
            return True
        return False

    def check_balance(self):
        return self.balance

    def change_password(self, old_password, new_password):
        if self.password == old_password and len(new_password) == 4:
            self.password = new_password
            return True
        return False

class ATM_GUI:
    def __init__(self, root, account_manager):
        self.root = root
        self.root.title("ATM Interface")
        self.atm = None
        self.account_manager = account_manager
        
        self.style = ttk.Style()
        self.style.configure("TLabel", font=("Arial", 12))
        self.style.configure("TButton", font=("Arial", 12))
        self.style.configure("TEntry", font=("Arial", 12))

        self.create_login_interface()

    def create_login_interface(self):
        self.clear_interface()

        ttk.Label(self.root, text="Enter Last 4 Digits of Card Number:").pack(pady=10)
        self.card_entry = ttk.Entry(self.root)
        self.card_entry.pack(pady=10)

        ttk.Label(self.root, text="Enter 4 Digit Password:").pack(pady=10)
        self.password_entry = ttk.Entry(self.root, show='*')
        self.password_entry.pack(pady=10)

        ttk.Button(self.root, text="Login", command=self.login).pack(pady=10)
        ttk.Button(self.root, text="Create Account", command=self.create_account_interface).pack(pady=10)

    def login(self):
        card_number = self.card_entry.get()
        password = self.password_entry.get()
        
        account = self.account_manager.get_account(card_number)
        if account and account['password'] == password:
            self.atm = ATM(card_number, password, account['balance'])
            self.create_main_interface()
        else:
            messagebox.showerror("Error", "Invalid Card Number or Password")

    def create_main_interface(self):
        self.clear_interface()

        ttk.Button(self.root, text="Deposit", command=self.deposit_interface).pack(pady=10)
        ttk.Button(self.root, text="Withdraw", command=self.withdraw_interface).pack(pady=10)
        ttk.Button(self.root, text="Check Balance", command=self.check_balance).pack(pady=10)
        ttk.Button(self.root, text="Change Password", command=self.change_password_interface).pack(pady=10)
        ttk.Button(self.root, text="Logout", command=self.logout).pack(pady=10)

    def clear_interface(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def deposit_interface(self):
        self.clear_interface()
        ttk.Label(self.root, text="Enter Amount to Deposit:").pack(pady=10)
        self.amount_entry = ttk.Entry(self.root)
        self.amount_entry.pack(pady=10)
        ttk.Button(self.root, text="Deposit", command=self.deposit).pack(pady=10)
        ttk.Button(self.root, text="Back", command=self.create_main_interface).pack(pady=10)

    def deposit(self):
        amount = float(self.amount_entry.get())
        if self.atm.deposit(amount):
            self.account_manager.accounts[self.atm.card_number]['balance'] = self.atm.check_balance()
            self.account_manager.save_accounts()
            messagebox.showinfo("Success", f"Deposited {amount}")
        else:
            messagebox.showerror("Error", "Invalid Amount")
        self.create_main_interface()

    def withdraw_interface(self):
        self.clear_interface()
        ttk.Label(self.root, text="Enter Amount to Withdraw:").pack(pady=10)
        self.amount_entry = ttk.Entry(self.root)
        self.amount_entry.pack(pady=10)
        ttk.Button(self.root, text="Withdraw", command=self.withdraw).pack(pady=10)
        ttk.Button(self.root, text="Back", command=self.create_main_interface).pack(pady=10)

    def withdraw(self):
        amount = float(self.amount_entry.get())
        if self.atm.withdraw(amount):
            self.account_manager.accounts[self.atm.card_number]['balance'] = self.atm.check_balance()
            self.account_manager.save_accounts()
            messagebox.showinfo("Success", f"Withdrew {amount}")
        else:
            messagebox.showerror("Error", "Insufficient Balance or Invalid Amount")
        self.create_main_interface()

    def check_balance(self):
        balance = self.atm.check_balance()
        messagebox.showinfo("Balance", f"Your balance is {balance}")

    def change_password_interface(self):
        self.clear_interface()
        ttk.Label(self.root, text="Enter Old Password:").pack(pady=10)
        self.old_password_entry = ttk.Entry(self.root, show='*')
        self.old_password_entry.pack(pady=10)

        ttk.Label(self.root, text="Enter New Password:").pack(pady=10)
        self.new_password_entry = ttk.Entry(self.root, show='*')
        self.new_password_entry.pack(pady=10)

        ttk.Button(self.root, text="Change Password", command=self.change_password).pack(pady=10)
        ttk.Button(self.root, text="Back", command=self.create_main_interface).pack(pady=10)

    def change_password(self):
        old_password = self.old_password_entry.get()
        new_password = self.new_password_entry.get()
        if self.atm.change_password(old_password, new_password):
            self.account_manager.accounts[self.atm.card_number]['password'] = new_password
            self.account_manager.save_accounts()
            messagebox.showinfo("Success", "Password Changed Successfully")
        else:
            messagebox.showerror("Error", "Invalid Password or New Password is not 4 digits")
        self.create_main_interface()

    def logout(self):
        self.atm = None
        self.create_login_interface()

    def create_account_interface(self):
        self.clear_interface()

        ttk.Label(self.root, text="Enter Last 4 Digits of Card Number:").pack(pady=10)
        self.card_entry = ttk.Entry(self.root)
        self.card_entry.pack(pady=10)

        ttk.Label(self.root, text="Enter 4 Digit Password:").pack(pady=10)
        self.password_entry = ttk.Entry(self.root, show='*')
        self.password_entry.pack(pady=10)

        ttk.Button(self.root, text="Create Account", command=self.create_account).pack(pady=10)
        ttk.Button(self.root, text="Back", command=self.create_login_interface).pack(pady=10)

    def create_account(self):
        card_number = self.card_entry.get()
        password = self.password_entry.get()

        if len(card_number) == 4 and len(password) == 4:
            if self.account_manager.create_account(card_number, password):
                messagebox.showinfo("Success", "Account Created Successfully")
                self.create_login_interface()
            else:
                messagebox.showerror("Error", "Account Already Exists")
        else:
            messagebox.showerror("Error", "Card Number and Password must be 4 digits each")

if __name__ == "__main__":
    account_manager = AccDetails('accounts.json')
    root = tk.Tk()
    app = ATM_GUI(root, account_manager)
    root.mainloop()