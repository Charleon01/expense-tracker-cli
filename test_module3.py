from db_helper import add_expense,get_user_expenses_detailed

# 1. Add fresh expenses for User 1 (Alice)
# User 1, Category 1 (Groceries), $45.20
add_expense(user_id=1, category_id=1, amount=45.20, note="Supermarket run")

# User 1, Category 3 (Dinning Out), $18.50
add_expense(user_id=1, category_id=3, amount=18.50, note="Coffee & pastries")

print("/n--- Detailed Expense Report for User 1---")

expenses = get_user_expenses_detailed(1)

for exp in expenses:
    expense_id, email, category, trans_type, amount, date, note= exp
    print(f"ID: {expense_id} | User: {email} | Category: {category} [{trans_type}] | Amount ${amount:.2f} | Date: {date} | Note: {note}")