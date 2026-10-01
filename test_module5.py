from db_helper import add_expense, get_monthly_spending_report, get_weekly_spending_report

add_expense(user_id=1, category_id=1, amount=120.00, note="August Groceries", transaction_date="2026-08-15")
add_expense(user_id=1, category_id=3, amount=85.50, note="August Dinner", transaction_date="2026-08-20")

print("---Monthly Spending Breakdown---")
monthly_data = get_monthly_spending_report(1)

for row in monthly_data:
    month, count, total = row
    print(f"Month: {month} | Transactions: {count} | Total Spent: ${total:.2f}")


print("\n---Weekly Spending Breaking---")
weekly_data = get_weekly_spending_report(1)

for row in weekly_data:
    week, count, total =row
    print(f"Week: {week} | Transactions: {count} | Total Spent: ${total:.2f}")