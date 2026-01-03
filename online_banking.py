# ---------- Custom Exceptions ----------
class InsufficientBalanceError(Exception): pass
class InvalidAmountError(Exception): pass
class AccountNotFoundError(Exception): pass
class TransactionLimitError(Exception): pass
class InvalidPinError(Exception): pass
class AccountLockedError(Exception): pass
class DailyLimitExceededError(Exception): pass


# ---------- Wallet System ----------
class WalletSystem:
    def __init__(self):
        self.accounts = {}  
        self.transaction_limit = 50000
        self.daily_limit = 100000

    def create_account(self, acc_no, pin, balance):
        if balance < 0:
            raise InvalidAmountError("Initial balance cannot be negative")
        self.accounts[acc_no] = {
            "balance": balance,
            "pin": pin,
            "attempts": 0,
            "locked": False,
            "daily_spent": 0,
            "history": []
        }
        print("✅ Account created successfully")

    def authenticate(self, acc_no, pin):
        acc = self.accounts.get(acc_no)
        if not acc:
            raise AccountNotFoundError("Account not found")
        if acc["locked"]:
            raise AccountLockedError("Account is locked")

        if acc["pin"] != pin:
            acc["attempts"] += 1
            if acc["attempts"] >= 3:
                acc["locked"] = True
                raise AccountLockedError("Account locked due to 3 failed attempts")
            raise InvalidPinError("Invalid PIN")

        acc["attempts"] = 0

    def deposit(self, acc_no, pin, amount):
        self.authenticate(acc_no, pin)
        if amount <= 0:
            raise InvalidAmountError("Deposit amount must be positive")

        self.accounts[acc_no]["balance"] += amount
        self.accounts[acc_no]["history"].append(f"Deposited ₹{amount}")
        print("💰 Deposit successful")

    def withdraw(self, acc_no, pin, amount):
        self.authenticate(acc_no, pin)
        acc = self.accounts[acc_no]

        if amount <= 0:
            raise InvalidAmountError("Invalid withdrawal amount")
        if amount > self.transaction_limit:
            raise TransactionLimitError("Transaction limit exceeded")
        if acc["daily_spent"] + amount > self.daily_limit:
            raise DailyLimitExceededError("Daily limit exceeded")
        if acc["balance"] < amount:
            raise InsufficientBalanceError("Insufficient balance")

        acc["balance"] -= amount
        acc["daily_spent"] += amount
        acc["history"].append(f"Withdrawn ₹{amount}")
        print("💸 Withdrawal successful")

    def transfer(self, from_acc, pin, to_acc, amount):
        self.authenticate(from_acc, pin)
        if to_acc not in self.accounts:
            raise AccountNotFoundError("Receiver account not found")

        self.withdraw(from_acc, pin, amount)
        self.accounts[to_acc]["balance"] += amount
        self.accounts[from_acc]["history"].append(
            f"Transferred ₹{amount} to {to_acc}"
        )
        print("🔁 Transfer successful")

    def show_balance(self, acc_no, pin):
        self.authenticate(acc_no, pin)
        print(f"📊 Balance: ₹{self.accounts[acc_no]['balance']}")

    def show_history(self, acc_no, pin):
        self.authenticate(acc_no, pin)
        print("📜 Transaction History:")
        for h in self.accounts[acc_no]["history"][-5:]:
            print("-", h)

    def close_account(self, acc_no, pin):
        self.authenticate(acc_no, pin)
        del self.accounts[acc_no]
        print("❌ Account closed successfully")


# ---------- Main Menu ----------
wallet = WalletSystem()

while True:
    print("\n===== ADVANCED ONLINE BANKING SYSTEM =====")
    print("1. Create Account")
    print("2. Deposit")
    print("3. Withdraw")
    print("4. Transfer")
    print("5. Check Balance")
    print("6. Transaction History")
    print("7. Close Account")
    print("8. Exit")

    try:
        choice = int(input("Enter choice: "))

        if choice == 1:
            acc = int(input("Account number: "))
            pin = int(input("Set 4-digit PIN: "))
            bal = float(input("Initial balance: "))
            wallet.create_account(acc, pin, bal)

        elif choice == 2:
            acc = int(input("Account number: "))
            pin = int(input("PIN: "))
            amt = float(input("Amount: "))
            wallet.deposit(acc, pin, amt)

        elif choice == 3:
            acc = int(input("Account number: "))
            pin = int(input("PIN: "))
            amt = float(input("Amount: "))
            wallet.withdraw(acc, pin, amt)

        elif choice == 4:
            f = int(input("From account: "))
            pin = int(input("PIN: "))
            t = int(input("To account: "))
            amt = float(input("Amount: "))
            wallet.transfer(f, pin, t, amt)

        elif choice == 5:
            acc = int(input("Account number: "))
            pin = int(input("PIN: "))
            wallet.show_balance(acc, pin)

        elif choice == 6:
            acc = int(input("Account number: "))
            pin = int(input("PIN: "))
            wallet.show_history(acc, pin)

        elif choice == 7:
            acc = int(input("Account number: "))
            pin = int(input("PIN: "))
            wallet.close_account(acc, pin)

        elif choice == 8:
            print("👋 Exiting system")
            break

        else:
            print("❌ Invalid option")

    except (InvalidAmountError, InsufficientBalanceError,
            AccountNotFoundError, TransactionLimitError,
            InvalidPinError, AccountLockedError,
            DailyLimitExceededError) as e:
        print("Error:", e)

    except ValueError:
        print("❌ Invalid numeric input")

    except Exception as e:
        print("❌ Unexpected Error:", e)
