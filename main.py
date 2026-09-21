import mysql.connector
from decimal import Decimal
from datetime import datetime, timedelta
class Bank:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="sql@123",
            database="bank_database")
        self.cursor = self.conn.cursor()
        print("Database connected successfully!")

    def create_account(self):
        self.name = input("Enter your Name: ").strip()
        if not self.name or not self.name.isalpha():
            print("Name should not be empty!!")
            return
        self.account_type = input("Enter your account type (Savings or Current): ").strip().title()
        if self.account_type not in ("Savings", "Current"):
            print("Please enter a valid account type (Savings or Current)")
            return
        if self.account_type == "Savings":
            self.minimum_balance = 2000
        else:
            self.minimum_balance = 10000
        self.phone_number = input("Enter your valid phone number: ").strip()
        if not self.phone_number.isdigit() or len(self.phone_number) != 10:
            print("Please enter a valid 10-digit phone number")
            return
        self.pin_number=input("Enter your 4-digit PIN: ").strip()
        if not self.pin_number.isdigit() or len(self.pin_number) != 4:
            print("PIN must contain exactly 4 digits")
            return
        confirm_pin = input("Confirm your PIN: ").strip()
        if self.pin_number != confirm_pin:
            print("PINs do not match")
            return
        self.balance_amount = self.minimum_balance
        query = """
        INSERT INTO accounts
        (name, account_type, min_balance, balance, pin, phone_number)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        values=(self.name,self.account_type,self.minimum_balance,self.balance_amount,self.pin_number,self.phone_number)
        self.cursor.execute(query, values)
        self.conn.commit()
        self.account_number = self.cursor.lastrowid
        print("="*45)
        print("      ACCOUNT CREATED SUCCESSFULLY")
        print("="*45)
        print(f"Account Number    : {self.account_number}")
        print(f"Account Holder    : {self.name}")
        print(f"Account Type      : {self.account_type}")
        print(f"Minimum Balance   : ₹{self.minimum_balance:.2f}")
        print(f"Current Balance   : ₹{self.balance_amount:.2f}")
        print(f"Mobile Number     : {self.phone_number}")
        print("Account Status    : ACTIVE")
        print("="*45)

    def deposit(self):
        identifier=input("Enter Account Number or Mobile Number: ").strip()
        account=self.find_account(identifier)
        if not account:
            print("Account not found!")
            return
        if not self.check_account_lock(account):
            return
        if not self.check_transaction_limit(account[0]):
            return
        self.dp_amount=input("Enter amount to deposit: ").strip()
        if not self.dp_amount.isdigit():
            print("Please enter a valid amount!")
            return
        self.dp_amount=Decimal(self.dp_amount)
        if self.dp_amount<=0:
            print("Deposit amount must be greater than 0!")
            return
        for attempt in range(3):
            pin=input("Enter your PIN: ").strip()
            if pin==account[5]:
                query="""
                    UPDATE accounts SET failed_attempts=0
                    WHERE account_number=%s
                """
                self.cursor.execute(query,(account[0],))
                new_balance=account[4]+self.dp_amount
                query="""
                    UPDATE accounts SET balance=%s
                    WHERE account_number=%s
                """
                self.cursor.execute(query,(new_balance,account[0]))
                query="""
                    INSERT INTO transactions
                    (account_number,transaction_type,amount,transaction_date)
                    VALUES(%s,%s,%s,%s)
                """
                self.cursor.execute(query,(account[0],"DEPOSIT",self.dp_amount,datetime.now()))
                self.conn.commit()
                print("="*45)
                print("         DEPOSIT SUCCESSFUL")
                print("="*45)
                print(f"Account Number : {account[0]}")
                print(f"Deposited      : ₹{self.dp_amount:.2f}")
                print(f"New Balance    : ₹{new_balance:.2f}")
                print("="*45)
                return
            else:
                print("Incorrect PIN!")
                remaining=2-attempt
                if remaining>0:
                    print(f"Attempts remaining: {remaining}")
        locked_until=datetime.now()+timedelta(hours=1)
        query="""
            UPDATE accounts
            SET failed_attempts=3,
                account_status='LOCKED',
                locked_until=%s
            WHERE account_number=%s
        """
        self.cursor.execute(query,(locked_until,account[0]))
        self.conn.commit()
        print("="*45)
        print("          ACCOUNT LOCKED")
        print("="*45)
        print("Reason      : 3 incorrect PIN attempts")
        print("Locked For  : 1 Hour")
        print(f"Locked Until: {locked_until}")
        print("="*45)

    def withdraw(self):
        identifier=input("Enter Account Number or Mobile Number: ").strip()
        account=self.find_account(identifier)
        if not account:
            print("Account not found!")
            return
        if not self.check_account_lock(account):
            return
        self.wd_amount=input("Enter amount to withdraw: ").strip()
        if not self.wd_amount.isdigit():
            print("Please enter a valid amount!")
            return
        self.wd_amount=Decimal(self.wd_amount)
        if self.wd_amount<=0:
            print("Withdrawal amount must be greater than 0!")
            return
        available_amount=account[4]-account[3]
        if self.wd_amount>available_amount:
            print("\nInsufficient balance!")
            print(f"Current Balance : ₹{account[4]}")
            print(f"Minimum Balance : ₹{account[3]}")
            print(f"Available Amount: ₹{available_amount}")
            return
        for attempt in range(3):
            pin=input("Enter your PIN: ").strip()
            if pin==account[5]:
                query="""
                    UPDATE accounts
                    SET failed_attempts=0
                    WHERE account_number=%s
                """
                self.cursor.execute(query,(account[0],))
                new_balance=account[4]-self.wd_amount
                query="""
                    UPDATE accounts
                    SET balance=%s
                    WHERE account_number=%s
                """
                self.cursor.execute(query,(new_balance,account[0]))
                query="""
                    INSERT INTO transactions
                    (account_number,transaction_type,amount,transaction_date)
                    VALUES(%s,%s,%s,%s)
                """
                self.cursor.execute(query,(account[0],"WITHDRAW",self.wd_amount,datetime.now()))
                self.conn.commit()
                print("="*45)
                print("        WITHDRAWAL SUCCESSFUL")
                print("="*45)
                print(f"Account Number : {account[0]}")
                print(f"Withdrawn      : ₹{self.wd_amount}")
                print(f"Remaining      : ₹{new_balance}")
                print("="*45)
                return
            else:
                print("Incorrect PIN!")
                remaining=2-attempt
                if remaining>0:
                    print(f"Attempts remaining: {remaining}")
        locked_until=datetime.now()+timedelta(hours=1)
        query="""
            UPDATE accounts
            SET failed_attempts=3,
                account_status='LOCKED',
                locked_until=%s
            WHERE account_number=%s
        """
        self.cursor.execute(query,(locked_until,account[0]))
        self.conn.commit()
        print("="*45)
        print("          ACCOUNT LOCKED")
        print("="*45)
        print("Reason      : 3 incorrect PIN attempts")
        print("Locked For  : 1 Hour")
        print(f"Locked Until: {locked_until}")
        print("="*45)

    def check_account_lock(self,account):
        if account[8]=="LOCKED":
            if account[9] is not None:
                current_time=datetime.now()
                if current_time<account[9]:
                    remaining_time=account[9]-current_time
                    print("="*45)
                    print("          ACCOUNT IS LOCKED")
                    print("="*45)
                    print(f"Account Number : {account[0]}")
                    print(f"Locked Until   : {account[9]}")
                    print(f"Remaining Time : {remaining_time}")
                    print("="*45)
                    return False
                else:
                    query="""
                    UPDATE accounts
                    SET account_status='ACTIVE',
                        failed_attempts=0,
                        locked_until=NULL
                    WHERE account_number=%s
                    """
                    self.cursor.execute(query,(account[0],))
                    self.conn.commit()
                    print("Account lock period completed.")
                    print("Account is now ACTIVE.")
                    return True
        return True
    
    def find_account(self, identifier):
        query = """
            SELECT * FROM accounts WHERE account_number = %s OR phone_number = %s
        """
        self.cursor.execute(query, (identifier, identifier))
        account = self.cursor.fetchone()
        return account
    
    def money_transfer(self):
        sender_id=input("Enter Sender Account Number or Mobile Number: ").strip()
        sender=self.find_account(sender_id)
        if not sender:
            print("Sender account not found!")
            return
        if not self.check_account_lock(sender):
            return
        receiver_id=input("Enter Receiver Account Number or Mobile Number: ").strip()
        receiver=self.find_account(receiver_id)
        if not receiver:
            print("Receiver account not found!")
            return
        if sender[0]==receiver[0]:
            print("Sender and Receiver accounts cannot be the same!")
            return
        amount=input("Enter amount to transfer: ").strip()
        if not amount.isdigit():
            print("Please enter a valid amount!")
            return
        amount=Decimal(amount)
        if amount<=0:
            print("Transfer amount must be greater than 0!")
            return
        available_amount=sender[4]-sender[3]
        if amount>available_amount:
            print("\nInsufficient balance!")
            print(f"Current Balance : ₹{sender[4]}")
            print(f"Minimum Balance : ₹{sender[3]}")
            print(f"Available Amount: ₹{available_amount}")
            return
        for attempt in range(3):
            pin=input("Enter Sender PIN: ").strip()
            if pin==sender[5]:
                new_sender_balance=sender[4]-amount
                new_receiver_balance=receiver[4]+amount
                query="""
                    UPDATE accounts
                    SET balance=%s,failed_attempts=0
                    WHERE account_number=%s
                """
                self.cursor.execute(query,(new_sender_balance,sender[0]))
                query="""
                    UPDATE accounts
                    SET balance=%s
                    WHERE account_number=%s
                """
                self.cursor.execute(query,(new_receiver_balance,receiver[0]))
                query="""
                    INSERT INTO transactions
                    (account_number,transaction_type,amount,transaction_date)
                    VALUES(%s,%s,%s,%s)
                """
                self.cursor.execute(query,(sender[0],"TRANSFER_OUT",amount,datetime.now()))
                self.cursor.execute(query,(receiver[0],"TRANSFER_IN",amount,datetime.now()))
                self.conn.commit()
                print("="*45)
                print("         TRANSFER SUCCESSFUL")
                print("="*45)
                print(f"Sender Account   : {sender[0]}")
                print(f"Receiver Account : {receiver[0]}")
                print(f"Transferred       : ₹{amount}")
                print(f"Sender Balance    : ₹{new_sender_balance}")
                print("="*45)
                return
            else:
                print("Incorrect PIN!")
                remaining=2-attempt
                if remaining>0:
                    print(f"Attempts remaining: {remaining}")
        locked_until=datetime.now()+timedelta(hours=1)
        query="""
            UPDATE accounts
            SET failed_attempts=3,
                account_status='LOCKED',
                locked_until=%s
            WHERE account_number=%s
        """
        self.cursor.execute(query,(locked_until,sender[0]))
        self.conn.commit()
        print("="*45
              )
        print("          ACCOUNT LOCKED")
        print("="*45)
        print("Reason      : 3 incorrect PIN attempts")
        print("Locked For  : 1 Hour")
        print(f"Locked Until: {locked_until}")
        print("="*45)

    def details(self):
        account_holder=input("Enter Your Account Number or Mobile Number: ").strip()
        account=self.find_account(account_holder)
        if not account:
            print("Account Not Found....!!")
            print("Please Enter proper account number or mobile number..!!!")
            return
        if not self.check_account_lock(account):
            return
        print("="*45)
        print("          ACCOUNT HOLDER DETAILS")
        print("="*45)
        print(f"Account Number   : {account[0]}")
        print(f"Account Holder   : {account[1]}")
        print(f"Account Type     : {account[2]}")
        print(f"Current Balance  : ₹{account[4]:.2f}")
        print(f"Mobile Number    : {account[6]}")
        print(f"Account Status   : {account[8]}")
        print(f"Locked Until     : {account[9]}")
        print(f"Created At       : {account[10]}")
        print("="*45)

    def transcation_history(self):
        identifier=input("Enter Account Number or Mobile Number: ").strip()
        account=self.find_account(identifier)
        if not account:
            print("Account Not Found....!!")
            print("Please Enter proper account number or mobile number..!!!")
            return
        if not self.check_account_lock(account):
            return
        query="""
            SELECT transaction_type,amount,transaction_date
            FROM transactions
            WHERE account_number=%s
            ORDER BY transaction_date DESC
        """
        self.cursor.execute(query,(account[0],))
        transactions=self.cursor.fetchall()
        if not transactions:
            print("No Transactions Found....!!")
            return
        print("="*45)
        print("         TRANSACTION HISTORY")
        print("="*45)
        print(f"Account Number : {account[0]}")
        print(f"Account Holder : {account[1]}")
        print("="*45)
        for transaction in transactions:
            print(f"Type   : {transaction[0]}")
            print(f"Amount : ₹{transaction[1]:.2f}")
            print(f"Date   : {transaction[2]}")
            print("-"*45)
            0
    def changepin(self):
        choice=input("Do you remember your old PIN? (yes/no): ").strip().lower()
        if choice=="yes":
            account_num=input("Enter Your Account Number or Mobile Number: ").strip()
            account_holder=self.find_account(account_num)
            if not account_holder:
                print("Account is not found..!!!")
                return
            if not self.check_account_lock(account_holder):
                return
            self.pin=input("Enter OLD PIN Number: ").strip()
            if account_holder[5]!=self.pin:
                print("PIN Number does not match...!!!")
                return
        elif choice=="no":
            account_num=input("Enter Your Account Number or Mobile Number: ").strip()
            account_holder=self.find_account(account_num)
            if not account_holder:
                print("Account is not found..!!!")
                return
            if not self.check_account_lock(account_holder):
                return
        else:
            print("Please enter yes or no!")
            return
        self.new_pin=input("Enter new PIN Number: ").strip()
        if not self.new_pin.isdigit() or len(self.new_pin)!=4:
            print("PIN must contain exactly 4 digits")
            return
        confirm_pin=input("Confirm new PIN: ").strip()
        if self.new_pin!=confirm_pin:
            print("PINs do not match")
            return
        if self.new_pin==account_holder[5]:
            print("New PIN cannot be the same as old PIN")
            return
        query="""
        UPDATE accounts SET pin=%s,failed_attempts=0 WHERE account_number=%s
        """
        self.cursor.execute(query,(self.new_pin,account_holder[0]))
        self.conn.commit()
        print("Account PIN Number is changed successfully")
        
    def check_transaction_limit(self,account_number):
        today=datetime.now().date()
        query="""
        SELECT COUNT(*)
        FROM transactions
        WHERE account_number=%s
        AND DATE(transaction_date)=%s
        """
        self.cursor.execute(query,(account_number,today))
        count=self.cursor.fetchone()[0]
        if count>=3:
            print("="*45)
            print("       TRANSACTION LIMIT REACHED")
            print("="*45)
            print("Maximum 3 transactions are allowed per day.")
            print(f"Transactions Today : {count}")
            print("="*45)
            return False
        return True
b = Bank()
print("="*45)
print("      WELCOME TO BANKING SYSTEM ")
print("="*45)

while True:
    print(f"1. Create Account\n 2. Deposit\n 3. Withdraw\n 4. Money Transfer\n 5. Account Holder Details\n 6. Transaction History\n 7. Change PIN\n 8. Exit")
    choice = int(input("Enter your choice: "))
    if choice == 1:
        b.create_account()
    elif choice == 2:
        b.deposit()
    elif choice == 3:
        b.withdraw()
    elif choice == 4:
        b.money_transfer()
    elif choice == 5:
        b.details()
    elif choice == 6:
        b.transcation_history()
    elif choice == 7:
        b.changepin()
    elif choice == 8:
        break
    else:
        print("== PLEASE GIVE ME VALID INPUT OR CHOOSE FROM GIVEN OPTIONS ==")




