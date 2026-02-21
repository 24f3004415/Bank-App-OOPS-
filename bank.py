# bank.py
import json
import random
import string
from pathlib import Path


class Bank:
    database = "data.json"
    data = []

    # ================= LOAD DATABASE =================
    if Path(database).exists():
        with open(database, "r") as fs:
            data = json.load(fs)
    else:
        with open(database, "w") as fs:
            json.dump([], fs)

    @classmethod
    def __update(cls):
        with open(cls.database, "w") as fs:
            json.dump(cls.data, fs, indent=4)

    # ================= GENERATE UNIQUE ACCOUNT NO =================
    @staticmethod
    def __generateAccountNo():
        while True:
            numbers = random.choices(string.digits, k=4)
            letters = random.choices(string.ascii_letters, k=4)
            acc = numbers + letters
            random.shuffle(acc)
            acc_no = "".join(acc)

            # Ensure uniqueness
            if not any(user["account_no"] == acc_no for user in Bank.data):
                return acc_no

    # ================= CREATE ACCOUNT =================
    def create_account(self, name, age, email, pin, phone):

        # Validation
        if age < 18:
            return False, "User must be 18+"

        if len(str(pin)) != 4:
            return False, "PIN must be 4 digits"

        if len(str(phone)) != 10:
            return False, "Phone must be 10 digits"

        # Prevent duplicate email
        if any(user["email"] == email for user in Bank.data):
            return False, "Email already registered"

        account = {
            "name": name,
            "age": age,
            "email": email,
            "pin": pin,
            "phone": phone,
            "account_no": Bank.__generateAccountNo(),
            "balance": 0,
            "transactions": []
        }

        Bank.data.append(account)
        Bank.__update()

        return True, account["account_no"]

    # ================= AUTHENTICATE =================
    def authenticate(self, acc_no, pin):
        for user in Bank.data:
            if user["account_no"] == acc_no and user["pin"] == pin:
                return user
        return None

    # ================= DEPOSIT =================
    def deposit(self, user, amount):

        if amount <= 0:
            return False, "Amount must be positive"

        if amount > 10000:
            return False, "Deposit limit exceeded (10,000)"

        user["balance"] += amount
        user["transactions"].append(
            {"type": "Deposit", "amount": amount}
        )

        Bank.__update()
        return True, "Deposit successful"

    # ================= WITHDRAW =================
    def withdraw(self, user, amount):

        if amount <= 0:
            return False, "Amount must be positive"

        if amount > 10000:
            return False, "Withdraw limit exceeded (10,000)"

        if user["balance"] < amount:
            return False, "Insufficient balance"

        user["balance"] -= amount
        user["transactions"].append(
            {"type": "Withdraw", "amount": amount}
        )

        Bank.__update()
        return True, "Withdraw successful"

    # ================= DELETE =================
    def delete_account(self, user):
        Bank.data.remove(user)
        Bank.__update()
        return True

    # ================= UPDATE PROFILE =================
    def update_account(self, user, name, age, email, pin, phone):

        if age < 18:
            return False, "User must be 18+"

        if len(str(pin)) != 4:
            return False, "PIN must be 4 digits"

        if len(str(phone)) != 10:
            return False, "Phone must be 10 digits"

        # Check email uniqueness (if changed)
        for u in Bank.data:
            if u["email"] == email and u != user:
                return False, "Email already in use"

        user["name"] = name
        user["age"] = age
        user["email"] = email
        user["pin"] = pin
        user["phone"] = phone

        Bank.__update()
        return True, "Profile Updated Successfully"