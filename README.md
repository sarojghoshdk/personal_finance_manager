# Personal Finance Management Application - User Manual

# Overview
The Personal Finance Management Application is a command-line tool that helps users manage their finances. Key features include income and expense tracking, budget setting, financial reporting, and data backup. This guide provides instructions for installing, configuring, and using the application.

# Table of Contents
1.	Installation
2.	Setup
3.	Usage
4.	Main Features
5.	Data Backup and Restore
6.	Deleting Your Account
7.	Troubleshooting
8.	Database System
9.	Frequently Asked Questions (FAQ)

# Installation
## Prerequisites
•	Python 3.7+: The application requires Python version 3.7 or higher. Download Python here.
•	SQLite3: The app uses SQLite for database management, which is included with Python.
Step-by-Step Installation
### 1.	Clone or Download the Project
o	Clone the repository from GitHub or download it as a ZIP file and extract it.

-- git clone https://github.com/sarojghoshdk/personal_finance_manager.git


### 2.	Navigate to the Project Directory

-- cd personal_finance_manager

### 3.	 Install Required Python Packages
•	This project primarily uses built-in Python libraries, so no additional packages are required.
### 4.	 Run Initial Setup
•	Run the setup_db for the first time to initialize the database.

python setup_db.py


# Setup
Upon first launch, the app will create an SQLite database in the db/ folder (db/finance_manager.db). This database will store all user information, transactions, and budget data.
1.	Folder Structure:
o	app.py: The main application file.
o	db/: Folder containing the SQLite database.
o	db/backup/: Folder where backups are stored.
2.	Database Initialization:
o	The database will be initialized automatically with required tables when you first run the application.

# Usage
## To start the application, run:
			
python app.py


	Login and Registration
1.	Register: Enter a unique username and password to create an account.
2.	Login: Enter your username and password to access your account.



# Main Features
## 1. Add Transactions
•	Record income or expenses by entering the amount, category, date, and transaction type (income or expense).
## 2. Generate Financial Reports
•	Generate monthly or yearly financial reports to view total income, expenses, and savings for the selected period.
## 3. Set Budget
•	Set budget limits for specific categories (e.g., Food, Rent). The application will notify you when spending exceeds the budget for each category.
## 4. Delete Transaction
•	Enter the transaction ID to delete a transaction. This is useful for removing duplicate or incorrect entries.
## 5. Show Transactions
•	View a list of all transactions, including income and expenses, categorized for easy access.
## 6. Edit Transaction
•	Modify the details of an existing transaction, such as the amount, category, date, or type.
## 7. Export Transactions to CSV
•	Export all transaction data to a CSV file for analysis in spreadsheet software.
## 8. Income vs Expense Analysis
•	View total income versus total expenses for a selected period, giving insight into net savings or deficits.
## 9.View Summary 
•	Access a comprehensive dashboard summarizing your financial health, including total income, total expenses, net savings, and budget status.


# Data Backup and Restore
## Backup Data
•	Create a Backup: This feature saves a copy of your database to the db/backup folder.
o	In the main menu, select the Backup option to back up all data.
## Restore Data
•	Restore from Backup: This option restores data from the last backup.
o	In the main menu, select the Restore option to load data from a backup file.

# Deleting Your Account
If you wish to delete your account and all associated data, follow these steps:
1.	In the main menu, select the Delete Account option.
2.	Confirm your choice by typing yes when prompted. Warning: This action is irreversible.

# Frequently Asked Questions
## 1.	Q: Can I set a budget for each category?
o	A: Yes, you can set monthly budgets for specific categories, and the app will notify you when spending approaches or exceeds these limits.
## 2.	Q: Can I edit transactions after adding them?
o	A: Yes, you can use the Edit Transaction option to update any transaction details.
## 3.	Q: How can I view my spending habits over time?
o	A: Use the Generate Report and Income vs Expense Analysis options to review spending patterns.
## 4.	Q: Where is my data stored?
o	A: All data is stored locally in the SQLite database (db/finance_manager.db) in the project’s db/ folder.
