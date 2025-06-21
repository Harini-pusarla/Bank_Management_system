import json
import os

class Account:
    def __init__(self, name, account_number, balance=0):
        self.name = name
        self.account_number = account_number
        self.balance = balance

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            print(f"✅ Deposited ₹{amount}. New Balance: ₹{self.balance}")
        else:
            print("❌ Invalid deposit amount.")

    def withdraw(self, amount):
        if amount <= self.balance:
            self.balance -= amount
            print(f"✅ Withdrew ₹{amount}. New Balance: ₹{self.balance}")
        else:
            print("❌ Insufficient balance.")

    def view_balance(self):
        print(f"👤 Account: {self.name} | Balance: ₹{self.balance}")


class SavingsAccount(Account):
    def __init__(self, name, account_number, balance=0):
        super().__init__(name, account_number, balance)
        self.account_type = "Savings"

class CurrentAccount(Account):
    def __init__(self, name, account_number, balance=0):
        super().__init__(name, account_number, balance)
        self.account_type = "Current"

DATA_FILE = "accounts.json"

def load_accounts():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r") as file:
        return json.load(file)

def save_accounts(data):
    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)

def create_account():
    name = input("Enter your name: ")
    acc_type = input("Account Type (Savings/Current): ").capitalize()
    account_number = input("Enter new Account Number: ")
    initial_balance = float(input("Initial Deposit: "))

    if acc_type == "Savings":
        account = SavingsAccount(name, account_number, initial_balance)
    elif acc_type == "Current":
        account = CurrentAccount(name, account_number, initial_balance)
    else:
        print("❌ Invalid account type.")
        return

    data = load_accounts()
    data[account_number] = {
        "name": name,
        "type": acc_type,
        "balance": account.balance
    }
    save_accounts(data)
    print(f"✅ {acc_type} Account created successfully!")

def get_account(account_number):
    data = load_accounts()
    if account_number in data:
        acc = data[account_number]
        if acc["type"] == "Savings":
            return SavingsAccount(acc["name"], account_number, acc["balance"])
        else:
            return CurrentAccount(acc["name"], account_number, acc["balance"])
    else:
        print("❌ Account not found.")
        return None

def update_account(account):
    data = load_accounts()
    data[account.account_number]["balance"] = account.balance
    save_accounts(data)

def menu():
    while True:
        print("\n🔹 Bank Management Menu 🔹")
        print("1. Create Account")
        print("2. Deposit")
        print("3. Withdraw")
        print("4. View Balance")
        print("5. Exit")

        choice = input("Select an option: ")

        if choice == "1":
            create_account()

        elif choice == "2":
            acc_no = input("Enter Account Number: ")
            acc = get_account(acc_no)
            if acc:
                amount = float(input("Enter amount to deposit: "))
                acc.deposit(amount)
                update_account(acc)

        elif choice == "3":
            acc_no = input("Enter Account Number: ")
            acc = get_account(acc_no)
            if acc:
                amount = float(input("Enter amount to withdraw: "))
                acc.withdraw(amount)
                update_account(acc)

        elif choice == "4":
            acc_no = input("Enter Account Number: ")
            acc = get_account(acc_no)
            if acc:
                acc.view_balance()

        elif choice == "5":
            print("👋 Exiting... Thank you!")
            break
        else:
            print("❌ Invalid choice. Try again.")

if __name__ == "__main__":
    menu()