from db_helper import add_expense, get_total_spent_by_category, get_categories_above_budget

add_expense(user_id=1, category_id=1, amount=30.00, note="Groceries mid-week")
add_expense(user_id=1, category_id=3, amount=55.00, note="Dinner with friends")

print("---Category Spending Summary ---")
summary = get_total_spent_by_category(1)

for row in summary:
    category, count, total, avg = row 
    print(f"Category: {category:<12} | Transactions: {count} | Total Spent: ${total:.2f} | Avg: ${avg:.2f}")


print("\n--- High Spending Categories (> $50) ---")
high_spending = get_categories_above_budget(user_id=1, threshold=50.00)

for row in high_spending:
    print(f"Alert: {row[0]} threshold exceeded! Total: ${row[1]:.2f}")