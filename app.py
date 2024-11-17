import sqlite3
import bcrypt
from datetime import datetime
import shutil
import os
import csv
import matplotlib.pyplot as plt


# Database Connection
def get_db_connection():
    return sqlite3.connect('db/finance_manager.db')

# User Registration
def register_user(username, password):
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, hashed_password) VALUES (?, ?)", (username, hashed_password))
        conn.commit()
        print("User registered successfully.")
    except sqlite3.IntegrityError:
        print("Username already exists.")
    conn.close()

# User Authentication
def authenticate_user(username, password):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()
    if user and bcrypt.checkpw(password.encode('utf-8'), user[2]):
        print("Login successful.")
        return user[0]  # Return user_id
    else:
        print("Invalid credentials.")
        return None

# Add Transaction
def add_transaction(user_id, amount, category, date, transaction_type):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO transactions (user_id, amount, category, date, type) VALUES (?, ?, ?, ?, ?)",
                   (user_id, amount, category, date, transaction_type))
    conn.commit()
    conn.close()
    print(f"{transaction_type.capitalize()} added successfully.")

# Generate Financial Report
def generate_report(user_id, period):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT SUM(amount) FROM transactions WHERE user_id = ? AND date LIKE ? AND type = 'income'",
                   (user_id, f"{period}-%"))
    total_income = cursor.fetchone()[0] or 0
    cursor.execute("SELECT SUM(amount) FROM transactions WHERE user_id = ? AND date LIKE ? AND type = 'expense'",
                   (user_id, f"{period}-%"))
    total_expenses = cursor.fetchone()[0] or 0
    savings = total_income - total_expenses
    conn.close()
    print(f"Report for {period}:\nTotal Income: {total_income}\nTotal Expenses: {total_expenses}\nSavings: {savings}")

# Set Budget
def set_budget(user_id, category, amount):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT OR REPLACE INTO budgets (user_id, category, amount) VALUES (?, ?, ?)", (user_id, category, amount))
    conn.commit()
    conn.close()
    print(f"Budget set for category '{category}'.")

# Check Budget Limit
def check_budget(user_id, category, amount):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT amount FROM budgets WHERE user_id = ? AND category = ?", (user_id, category))
    budget = cursor.fetchone()
    if budget and amount > budget[0]:
        print(f"Warning: Exceeded budget for category '{category}'.")
    conn.close()

# Backup and Restore
def backup_data():
    # Ensure the backup directory exists
    os.makedirs('db/backup', exist_ok=True)
    
    # Perform the backup
    shutil.copy('db/finance_manager.db', 'db/backup/finance_manager_backup.db')
    print("Backup completed.")

def restore_data():
    # Ensure the backup file exists before restoring
    backup_file = 'db/backup/finance_manager_backup.db'
    if os.path.exists(backup_file):
        shutil.copy(backup_file, 'db/finance_manager.db')
        print("Restore completed.")
    else:
        print("No backup found to restore.")

# Delete Transaction
def delete_transaction(user_id, transaction_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Check if the transaction exists and belongs to the user
    cursor.execute("SELECT * FROM transactions WHERE id = ? AND user_id = ?", (transaction_id, user_id))
    transaction = cursor.fetchone()
    
    if transaction:
        # Delete the transaction
        cursor.execute("DELETE FROM transactions WHERE id = ? AND user_id = ?", (transaction_id, user_id))
        conn.commit()
        print("Transaction deleted successfully.")
    else:
        print("Transaction not found or you do not have permission to delete this transaction.")
    
    conn.close()

# Show Transactions
def show_transactions(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Retrieve all transactions for the user
    cursor.execute("SELECT id, amount, category, date, type FROM transactions WHERE user_id = ?", (user_id,))
    transactions = cursor.fetchall()
    
    if transactions:
        print("\nYour Transactions:")
        print("ID\tAmount\tCategory\tDate\t\tType")
        print("-" * 50)
        for transaction in transactions:
            print(f"{transaction[0]}\t{transaction[1]}\t{transaction[2]}\t{transaction[3]}\t{transaction[4]}")
    else:
        print("No transactions found.")
    
    conn.close()

# Edit Transaction
def edit_transaction(user_id, transaction_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Check if the transaction exists and belongs to the user
    cursor.execute("SELECT * FROM transactions WHERE id = ? AND user_id = ?", (transaction_id, user_id))
    transaction = cursor.fetchone()
    
    if transaction:
        print("Enter new details for the transaction (leave blank to keep current value):")
        
        # Get new values from the user
        new_amount = input(f"Amount [{transaction[2]}]: ")
        new_category = input(f"Category [{transaction[3]}]: ")
        new_date = input(f"Date (YYYY-MM-DD) [{transaction[4]}]: ")
        new_type = input(f"Type (income/expense) [{transaction[5]}]: ")
        
        # Use the existing values if the input is blank
        new_amount = float(new_amount) if new_amount else transaction[2]
        new_category = new_category if new_category else transaction[3]
        new_date = new_date if new_date else transaction[4]
        new_type = new_type if new_type else transaction[5]
        
        # Update the transaction with the new values
        cursor.execute("""
            UPDATE transactions
            SET amount = ?, category = ?, date = ?, type = ?
            WHERE id = ? AND user_id = ?
        """, (new_amount, new_category, new_date, new_type, transaction_id, user_id))
        
        conn.commit()
        print("Transaction updated successfully.")
    else:
        print("Transaction not found or you do not have permission to edit this transaction.")
    
    conn.close()

# Export Transactions to CSV
def export_transactions_to_csv(username):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Retrieve all transactions for the user
    cursor.execute("SELECT id, amount, category, date, type FROM transactions WHERE user_id = ?", (username,))
    transactions = cursor.fetchall()
    
    if transactions:
        # Define CSV file path
        file_path = f"transactions_export_{username}.csv"
        
        # Write transactions to CSV
        with open(file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["ID", "Amount", "Category", "Date", "Type"])  # Write header
            
            # Write transaction rows
            for transaction in transactions:
                writer.writerow(transaction)
        
        print(f"Transactions exported successfully to {file_path}.")
    else:
        print("No transactions found to export.")
    
    conn.close()

# Income vs. Expense Analysis
def income_vs_expense_analysis(user_id, period):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Determine the period for monthly or yearly analysis
    if len(period) == 7:  # Monthly format (YYYY-MM)
        cursor.execute("""
            SELECT type, SUM(amount)
            FROM transactions
            WHERE user_id = ? AND strftime('%Y-%m', date) = ?
            GROUP BY type
        """, (user_id, period))
    elif len(period) == 4:  # Yearly format (YYYY)
        cursor.execute("""
            SELECT type, SUM(amount)
            FROM transactions
            WHERE user_id = ? AND strftime('%Y', date) = ?
            GROUP BY type
        """, (user_id, period))
    else:
        print("Invalid period format. Use YYYY-MM for monthly or YYYY for yearly.")
        conn.close()
        return
    
    # Fetch results and calculate totals
    results = cursor.fetchall()
    income = sum(amount for type_, amount in results if type_ == 'income')
    expenses = sum(amount for type_, amount in results if type_ == 'expense')
    
    print(f"Income vs. Expense Analysis for {period}:")
    print(f"Total Income: {income}")
    print(f"Total Expenses: {expenses}")
    print(f"Net Savings: {income - expenses}")
    
    # Plot income vs expenses
    labels = ['Income', 'Expenses']
    values = [income, expenses]
    plt.bar(labels, values, color=['green', 'red'])
    plt.title(f"Income vs. Expenses for {period}")
    plt.xlabel('Type')
    plt.ylabel('Amount')
    plt.show()
    
    conn.close()


# Display Summary Dashboard
def display_dashboard(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Calculate total income
    cursor.execute("""
        SELECT SUM(amount) FROM transactions
        WHERE user_id = ? AND type = 'income'
    """, (user_id,))
    total_income = cursor.fetchone()[0] or 0  # Default to 0 if no income transactions

    # Calculate total expenses
    cursor.execute("""
        SELECT SUM(amount) FROM transactions
        WHERE user_id = ? AND type = 'expense'
    """, (user_id,))
    total_expenses = cursor.fetchone()[0] or 0  # Default to 0 if no expense transactions
    
    # Calculate net savings
    net_savings = total_income - total_expenses
    
    # Calculate budget utilization
    cursor.execute("""
        SELECT category, amount FROM budgets
        WHERE user_id = ?
    """, (user_id,))
    budgets = cursor.fetchall()

    budget_status = {}
    for category, budget_amount in budgets:
        cursor.execute("""
            SELECT SUM(amount) FROM transactions
            WHERE user_id = ? AND category = ? AND type = 'expense'
        """, (user_id, category))
        total_spent = cursor.fetchone()[0] or 0
        utilization = (total_spent / budget_amount) * 100 if budget_amount > 0 else 0
        budget_status[category] = (total_spent, budget_amount, utilization)
    
    # Display Dashboard
    print("\n--- Financial Summary Dashboard ---")
    print(f"Total Income: {total_income}")
    print(f"Total Expenses: {total_expenses}")
    print(f"Net Savings: {net_savings}")
    print("\n--- Budget Status ---")
    if not budget_status:
        print("No budgets set.")
    else:
        for category, (spent, budget, utilization) in budget_status.items():
            print(f"\nCategory: {category}")
            print(f"  Budget: {budget}")
            print(f"  Spent: {spent}")
            print(f"  Utilization: {utilization:.2f}%")
            if utilization > 100:
                print("  Warning: Budget exceeded!")
            elif utilization >= 80:
                print("  Caution: Approaching budget limit.")

    conn.close()

# Delete Account
def delete_account(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Confirmation prompt
    confirmation = input("Are you sure you want to delete your account and all associated data? This action is irreversible. (yes/no): ").strip().lower()
    if confirmation != 'yes':
        print("Account deletion cancelled.")
        conn.close()
        return
    
    # Delete all user-related data from the database
    try:
        # Delete transactions
        cursor.execute("DELETE FROM transactions WHERE user_id = ?", (user_id,))
        
        # Delete budgets
        cursor.execute("DELETE FROM budgets WHERE user_id = ?", (user_id,))

        # Delete user account
        cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))

        conn.commit()
        print("Your account and all associated data have been successfully deleted.")
    except Exception as e:
        conn.rollback()
        print("Error occurred while deleting account:", e)
    finally:
        conn.close()


# Main Application
def main():
    print("Welcome to Personal Finance Manager")
    user_id = None
    while True:
        print("\n1. Register\n2. Login\n3. Add Transaction\n4. Generate Report\n5. Set Budget\n6. Backup\n7. Restore\n8. Delete Transaction\n9. Show Transactions\n10. Edit Transaction\n11. Export Transactions to CSV\n12. Income vs Expense Analysis\n13. View Summary\n14. Delete Account\n15. Exit")
        choice = input("Select an option: ")
        
        if choice == '1':
            username = input("Username: ")
            password = input("Password: ")
            register_user(username, password)
        elif choice == '2':
            username = input("Username: ")
            password = input("Password: ")
            user_id = authenticate_user(username, password)
        elif choice == '3' and user_id:
            amount = float(input("Amount: "))
            category = input("Category: ")
            date = input("Date (YYYY-MM-DD): ")
            transaction_type = input("Type (income/expense): ")
            add_transaction(user_id, amount, category, date, transaction_type)
            check_budget(user_id, category, amount)
        elif choice == '4' and user_id:
            period = input("Enter period (YYYY-MM for monthly, YYYY for yearly): ")
            generate_report(user_id, period)
        elif choice == '5' and user_id:
            category = input("Category: ")
            amount = float(input("Budget amount: "))
            set_budget(user_id, category, amount)
        elif choice == '6':
            backup_data()
        elif choice == '7':
            restore_data()
        elif choice == '8' and user_id:
            transaction_id = int(input("Enter the transaction ID to delete: "))
            delete_transaction(user_id, transaction_id)
        elif choice == '9' and user_id:
            show_transactions(user_id)
        elif choice == '10' and user_id:
            transaction_id = int(input("Enter the transaction ID to edit: "))
            edit_transaction(user_id, transaction_id)
        elif choice == '11' and user_id:
            export_transactions_to_csv(user_id)
        elif choice == '12' and user_id:
            period = input("Enter period (YYYY-MM for monthly, YYYY for yearly): ")
            income_vs_expense_analysis(user_id, period)
        elif choice == '13' and user_id:
            display_dashboard(user_id)
        elif choice == '14' and user_id:
            delete_account(user_id)
            # Logout user after deletion
            user_id = None
        elif choice == '15':
            print("Exiting application.")
            break
        else:
            print("Invalid choice or unauthorized access (Please Login First to access the option 3 to 14).\n Please try again.")


if __name__ == "__main__":
    main()
