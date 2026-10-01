import sqlite3

conn = sqlite3.connect("tracker.db")
cursor = conn.cursor()

# Enable Foreign Key enforcement in SQLite (Required per connection!)
cursor.execute("PRAGMA foreign_keys = ON;")

# 1. Users Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
""")

# 2. Categories Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS categories (
    category_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,
    type TEXT CHECK(type IN ('expense', 'income')) NOT NULL
);
""")

# 3. Expenses Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS expenses (
    expense_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    category_id INTEGER NOT NULL,
    amount REAL NOT NULL CHECK(amount > 0),
    note TEXT,
    transaction_date DATE DEFAULT CURRENT_DATE,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (category_id) REFERENCES categories(category_id)
);
""")

print("All database tables (Users, Categories, Expenses) created successfully!")
conn.commit()
conn.close()