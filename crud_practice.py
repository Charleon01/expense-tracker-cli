import sqlite3

conn = sqlite3.connect("tracker.db")
cursor = conn.cursor()
cursor.execute("PRAGMA foreign_keys = ON;")

# Insert a Test User
cursor.execute("""
INSERT OR IGNORE INTO users (email) 
VALUES ('alice@example.com');
""")

# Insert Default Categories
cursor.execute("""
INSERT OR IGNORE INTO categories (name, type) 
VALUES 
    ('Groceries', 'expense'),
    ('Salary', 'income'),
    ('Dining Out', 'expense');
""")

# Insert an Expense linked to User ID 1 and Category ID 1 ('Groceries')
cursor.execute("""
INSERT INTO expenses (user_id, category_id, amount, note) 
VALUES (1, 1, 75.50, 'Weekly grocery run');
""")

conn.commit()
print("1. CREATE Success: inserted user, categories, ans expense.")

# Query expenses combined with category details
cursor.execute("""
SELECT e.expense_id, c.name, e.amount, e.note, e.transaction_date
FROM expenses e
JOIN categories c ON e.category_id = c.category_id
WHERE e.user_id = 1;
""")

rows = cursor.fetchall()

print("\n2. READ Success; Current records in database:")
for row in rows:
    print(f"  Expense ID: {row[0]} | Category: {row[1]} | Amount: ${row[2]} | Note: {row[3]} | Date: {row[4]}")


# Update amount for expense ID 1
cursor.execute("""
UPDATE expenses
SET amount = 82.25, note = 'Weekly grocery run + household items'
WHERE expense_id = 1;
""")

conn.commit()
print("\n3. UPDATE Success: updated Expense ID 1.")


# Delete specific expense
cursor.execute("""
DELETE FROM expenses
WHERE expense_id = 1;
""")

conn.commit()
print("\n4. DELETE Success: Cleaned up expense ID 1.")
conn.close()