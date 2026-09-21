# 🏦 Banking Management System

A simple and secure **Banking Management System** developed using **Python and MySQL**. This project provides basic banking operations such as account creation, deposits, withdrawals, money transfers, transaction history, account details, PIN management, and account locking.

## 📌 Project Overview

The Banking Management System is a console-based application designed to manage customer bank accounts and transactions.

The system uses **Python** for application logic and **MySQL** for storing account and transaction information.

## 🚀 Features

* Create a new bank account
* Savings and Current account support
* Minimum balance validation

  * Savings: ₹2,000
  * Current: ₹10,000
* Deposit money
* Withdraw money
* Money transfer between accounts
* Account holder details
* Transaction history
* Change PIN
* Forgot PIN functionality
* PIN validation
* Three incorrect PIN attempts lock the account
* Account locked for 1 hour after security violations
* Maximum 3 transactions per day
* Account identification using:

  * Account Number
  * Mobile Number
* Input validation for:

  * Name
  * Mobile number
  * PIN
  * Transaction amount
* Transaction date and time tracking using Python `datetime`
* MySQL transaction management with commit and rollback

## 🛠️ Technologies Used

| Technology      | Purpose                             |
| --------------- | ----------------------------------- |
| Python          | Application development             |
| MySQL           | Database management                 |
| MySQL Connector | Python-MySQL connection             |
| Decimal         | Accurate monetary calculations      |
| Datetime        | Transaction and account lock timing |

## 📂 Project Structure

```text
Banking-Management-System/
│
├── banking.py
├── README.md
└── requirements.txt
```

## 🗄️ Database

The project uses MySQL with two main tables:

### Accounts

Stores customer account information such as:

* Account Number
* Account Holder Name
* Account Type
* Minimum Balance
* Current Balance
* PIN
* Mobile Number
* Failed Attempts
* Account Status
* Locked Until
* Account Creation Date

### Transactions

Stores transaction information such as:

* Transaction ID
* Account Number
* Transaction Type
* Transaction Amount
* Transaction Date

## ⚙️ Requirements

Make sure the following are installed:

* Python 3.x
* MySQL Server
* MySQL Connector for Python

Install the required Python package:

```bash
pip install mysql-connector-python
```

## 🔧 Database Configuration

Update the MySQL connection details in the Python file:

```python
self.conn=mysql.connector.connect(
    host="localhost",
    user="root",
    password="your_password",
    database="your_database_name"
)
```

Replace:

```text
your_password
```

with your MySQL password.

Replace:

```text
your_database_name
```

with your existing database name.

## ▶️ How to Run

Clone the repository:

```bash
git clone https://github.com/your-username/Banking-Management-System.git
```

Open the project folder:

```bash
cd Banking-Management-System
```

Install the dependency:

```bash
pip install mysql-connector-python
```

Run the application:

```bash
python banking.py
```

## 📋 Main Menu

```text
=========================================
       WELCOME TO BANKING SYSTEM
=========================================

1. Create Account
2. Deposit
3. Withdraw
4. Money Transfer
5. Account Holder Details
6. Transaction History
7. Change PIN
8. Exit
```

## 🔐 Security Features

The application includes several security mechanisms:

### PIN Verification

Users must enter the correct 4-digit PIN before performing sensitive operations.

### Account Locking

If the user enters an incorrect PIN three consecutive times, the account is locked for one hour.

### Account Identification Validation

The system supports account identification using either an account number or registered mobile number.

### Transaction Limit

A maximum of **3 transactions per account per day** is allowed. The transaction count is validated using the transaction date and Python `datetime`.

### Minimum Balance

Users cannot withdraw or transfer an amount that would reduce their account balance below the required minimum balance.

## 💰 Banking Operations

### Create Account

The user provides:

```text
Name
Account Type
Mobile Number
PIN
```

The system automatically assigns an account number and sets the required minimum balance.

### Deposit

Users can deposit money by providing:

```text
Account Number / Mobile Number
Amount
PIN
```

### Withdraw

Users can withdraw money after successful account and PIN verification.

The system checks the available balance while maintaining the required minimum balance.

### Money Transfer

Money can be transferred from one account to another.

The system validates:

* Sender account
* Receiver account
* Sender PIN
* Available balance
* Minimum balance
* Transaction limit

### Transaction History

Users can view previous transactions associated with their account.

### Change PIN

Users can change their PIN by:

* Verifying the existing PIN, or
* Using the forgot PIN option with their account number or mobile number.

## 📊 Example Transaction Types

```text
DEPOSIT
WITHDRAW
TRANSFER_OUT
TRANSFER_IN
```

## 🔄 Error Handling

The application handles common errors such as:

* Invalid account number
* Invalid mobile number
* Invalid PIN
* Incorrect PIN
* Invalid transaction amount
* Insufficient balance
* Invalid account type
* Duplicate mobile number
* Database errors
* Locked accounts
* Transaction limit exceeded

Database operations use `commit()` for successful transactions and `rollback()` when an operation fails.

## 🎯 Learning Outcomes

This project demonstrates practical implementation of:

* Python OOP
* Classes and methods
* MySQL database connectivity
* SQL queries
* CRUD operations
* Exception handling
* Input validation
* Financial calculations using `Decimal`
* Date and time handling
* Transaction management
* Authentication and PIN validation
* Account security
* Database-driven application development

## 🔮 Future Enhancements

Possible improvements include:

* Graphical User Interface
* Web-based banking application
* Flask/Django integration
* OTP verification
* Email notifications
* SMS notifications
* Admin dashboard
* Password/PIN encryption
* PDF bank statements
* Online transaction APIs
* Advanced transaction reporting

