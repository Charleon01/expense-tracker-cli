import sys
from db_helper import (get_connection, add_expense, get_user_expenses_detailed, 
                       get_total_spent_by_category, get_monthly_spending_report,
                         get_all_categories, add_category, delete_category,
                           update_category_budget, check_budget_status, export_expenses_to_csv)

def display_menu():
    print("\n=============================")
    print("      EXPENSE TRACKER CLI      ")
    print("1. Add New Expense")
    print("2. View All Detailed Expenses")
    print("3. View Category Spending Summary")
    print("4. View Monthly Spending Report")
    print("5. Manage Category (View/Add/Delete)")
    print("6. Export Expenses to CSV")
    print("7. Exit")
    print("--------------------------------")


def handle_add_expense(user_id):
    print("\n--- Add New Expense ---")
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT category_id, name, type FROM categories ORDER BY type, name;")
    categories = cursor.fetchall()
    conn.close()

    print("Available Categories:")
    for cat in categories:
        print(f"   [{cat[0]}]  {cat[1]}  ({cat[2]})")

    try:
        category_id = int(input("\nEnter Category ID: "))
        amount = float(input("Enter Amount ($): "))
        note = input("Enter Note (optional, press Enter to skip): ").strip() or None

        add_expense(user_id=user_id, category_id=category_id, amount=amount, note=note)
        status= check_budget_status(user_id, category_id)
        if status:
            if status["is_exceeded"]:
                print (f"\n ALERT: You have EXCEEDED your budget for '{status['category_name']}'!")
                print (f"  Spent: ${status['total_spent']:.2f} / Budget: $ {status['budget_limit']:.2f}")
            else:
                remaining = status["budget_limit"] - status["total_spent"]
                print(f" Budget Status: $ {status['total_spent']:.2f} spent of ${status['budget_limit']:.2f} limit (${remaining:.2f} remaining).")

                
    
    except ValueError:
        print("Invalid input! Amount and Category ID must be numbers.")

def handle_view_expenses(user_id):
    print("\n--- All Detailed Expenses ---")
    expenses = get_user_expenses_detailed(user_id)
    if not expenses:
        print("No expenses logged yet.")
        return
    
    for exp in expenses:
       expense_id = exp[0]
       category_name = exp[1]
       trans_type = exp[2] if len(exp) > 2 else "expense"
       amount = exp[3] if len(exp) > 3 else 0.0
       date = exp[4] if len(exp) > 4 else ""
       note = exp[5] if (len(exp) > 5 and exp[5]) else "No note"

       print(f"ID: {expense_id} | Category: {category_name} [{trans_type}] | Amount: ${amount:.2f} | Date: {date} | Note: {note}")

def handle_category_summary(user_id):
    print("\n---Category Spending Summary ---")
    summary = get_total_spent_by_category(user_id)
    if not summary:
        print("No expenses logged yet.")
        return 
    
    for row in summary:
        print(f"Category: {row[0]:<12} | Transactions: {row[1]} | Total Spent: ${row[2]:.2f} | Avg: ${row[3]:.2f}")

def handle_monthly_report(user_id):
    print("\n---Monthly Spending Report---")
    report = get_monthly_spending_report(user_id)
    if not report:
        print("No expenses logged yet.")
        return
    
    for row in report:
        print(f"Month: {row[0]} | Transactions: {row[1]} | Total Spent: ${row[2]:.2f}")

def handle_category_management():
    while True:
        print("\n--- Category Management ---")
        print("1. View All Categories")
        print("2. Add New Category")
        print("3. Set/Update Category Monthly Budget")
        print("4. Delete Category")
        print("5. Back to Main Menu")

        choice= input("Select an option (1-5):").strip()

        if choice == '1':
            cats =get_all_categories()
            print("\n Existing Categories")
            for c in cats:
                budget_str = f"  | Budget: ${c[3]:.2f}" if len(c) > 3 and c[3] else ""
                print(f" ID: {c[0]} | Name: {c[1]} | Type: {c[2]}{budget_str}")
       
        elif choice == '2':
            name = input("Enter new category name:").strip()
            if name:
                cat_type = input("Enter type ('expense' or 'income', default='expense'):").strip() or "expense"
                add_category(name, cat_type)
            else:
                print("Category name cannot be empty.")
        
        elif choice == '3':
            try:
                cat_id = int(input("Enter Category ID to set budget for: "))
                budget = float(input("Enter Monthly Budget Limit ($): "))
                update_category_budget(cat_id, budget)

            except ValueError:
                print("Invalid input! Category ID! and Budget must be numbers.")
        elif choice == '4':
            try:
                cat_id = int(input("Enter Category ID to delete: "))
                delete_category(cat_id)
            except ValueError:
                print("Invalid Category ID!")

        elif choice == '5':
            break
        else:
            print("Invalid choice! Please select 1-5.")


def main():
    current_user_id = 1
    while True:
        display_menu()
        choice = input("Select an option (1-7):").strip()

        if choice == '1':
            handle_add_expense(current_user_id)
        elif choice == '2':
            handle_view_expenses(current_user_id)
        elif choice == '3':
            handle_category_summary(current_user_id)
        elif choice == '4':
            handle_monthly_report(current_user_id)
        elif choice == '5':
            handle_category_management()
        elif choice == '6':
            export_expenses_to_csv(current_user_id)
        elif choice == '7':
            print("\n Thank you for using Expense Tracker! Goodbye.")
            sys.exit()
        else:
            print("Invalid choice! Please select a number from 1 to 5.")

if __name__ == "__main__":
    main()
        