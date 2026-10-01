import sqlite3

DB_NAME = "tracker.db"

def get_connection():
    """Creates a database connection with foreign keys enabled."""
    conn = sqlite3.connect(DB_NAME)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def add_expense(user_id, category_id, amount, note=None, transaction_date=None):
    """Inserts a new expense into the database safely."""
    conn = get_connection()
    cursor = conn.cursor()
    
    query = """
    INSERT INTO expenses (user_id, category_id, amount, note, transaction_date)
    VALUES (?, ?, ?, ?, COALESCE(?, CURRENT_DATE));
    """
    
    try:
        cursor.execute(query, (user_id, category_id, amount, note, transaction_date))
        conn.commit()
        print(f"Expense of ${amount} added successfully!")
    except sqlite3.IntegrityError as e:
        print(f"Error: Invalid User ID or Category ID! Details: {e}")
    finally:
        conn.close()

def get_user_expenses_detailed(user_id):
    """
    Fetches expenses combined with category and usr names
    using INNER JOIN across expenses, categories, and users."""

    conn = get_connection()
    cursor = conn.cursor()

    query="""
    SELECT
        e.expense_id,
        u.email,
        c.name AS category_name,
        c.type AS transaction_date,
        e.transaction_date,
        e.note
    FROM expenses e
    INNER JOIN users u ON e.user_id = u.user_id  
    INNER JOIN categories c ON e.category_id = c.category_id
    WHERE e.user_id = ?
    ORDER BY e.transaction_date DESC;
    """

    cursor.execute(query, (user_id,))
    records = cursor.fetchall()
    conn.close()
    return records

def get_total_spent_by_category(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
    SELECT
        c.name AS category_name,
        COUNT(e.expense_id) AS total_transactions, 
        SUM(e.amount) AS category_total,
        ROUND(AVG(e.amount), 2) AS average_per_transaction
    FROM expenses e
    INNER JOIN categories c ON e.category_id = c.category_id
    WHERE e.user_id = ? AND c.type = 'expense'
    GROUP BY c.name
    ORDER BY category_total DESC;
    """

    cursor.execute(query, (user_id,))
    records = cursor.fetchall()
    conn.close()
    return records

def get_categories_above_budget(user_id,threshold):
    conn =  get_connection()
    cursor = conn.cursor()

    query = """
    SELECT
        c.name,
        SUM(e.amount) AS total_spent
    FROM expenses e
    INNER JOIN categories c ON e.category_id = c.category_id
    WHERE e.user_id = ?
    GROUP BY c.name
    HAVING total_spent > ?;
    """

    cursor.execute(query, (user_id, threshold))
    records = cursor.fetchall()
    conn.close()
    return records       

def get_monthly_spending_report(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
    SELECT
        strftime('%Y-%m', transaction_date) AS month,

        COUNT(expense_id) AS total_transactions,
        SUM(amount) AS monthly_total

    FROM expenses
    WHERE user_id = ? 
    GROUP BY month
    ORDER BY month DESC;
    """

    cursor.execute(query, (user_id,))
    records = cursor.fetchall()
    conn.close()
    return records

def get_weekly_spending_report(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
    SELECT
        strftime('%Y-W%W', transaction_date) AS week,

        COUNT(expense_id) AS total_transactions,
        SUM(amount) AS weekly_total
    FROM expenses 
    WHERE user_id = ?
    GROUP BY week
    ORDER BY week DESC;
    """

    cursor.execute(query, (user_id,))
    records = cursor.fetchall()
    conn.close()
    return records

def get_all_categories():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT category_id, name, type FROM categories ORDER BY type, name;")
    categories = cursor.fetchall()
    conn.close()
    return categories

def add_category(name, cat_type="expense"):
    conn = get_connection()
    cursor = conn.cursor()

    query = "INSERT INTO categories (name, type) VALUES (?, ?);"

    try:
        cursor.execute(query, (name, cat_type.lower()))
        conn.commit()
        print(f"Category '{name}' ({cat_type}) added successfully!")
    except Exception as e:
        print(f"Error adding category: {e}")
    finally:
        conn.close()

def delete_category(category_id):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("DELETE FROM categories WHERE categories_id = ?;", (category_id))
        conn.commit()
        print(f"Category ID {category_id} deleted successfully.")
    except Exception as e:
         print(f"Error deleting category:{e}")
    finally:
        conn.close()
        
def update_category_budget(category_id, budget_limit):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("ALTER TABLE categories ADD COLUMN budget_limit REAL DEFAULT 0.0;")
    except Exception:
        pass #Column alraedy exists
    query = "UPDATE categories SET budget_limit = ? WHERE category_id = ?;"
    cursor.execute(query, (budget_limit, category_id))
    conn.commit()
    conn.close()
    print(f"Budget limit of ${budget_limit:.2f} set for Category ID {category_id}.")

def check_budget_status(user_id, category_id):
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT name,  budget_limit FROM categories WHERE category_id = ?", (category_id,))
        row = cursor.fetchone()
    except Exception:
        conn.close()
        return None
    
    if not row or row[1] is None or row[1] <= 0:
            conn.close()
            return None 
    cat_name = row[0]
    budget_limit = row[1]#No budget limit set cat_name, budget_limit = row[0], row[1]
    
    
    query = """
    SELECT SUM(amount)
    FROM expenses
    WHERE user_id = ?
      AND category_id = ? 
      AND strftime('%Y-%m', transaction_date) = strftime('%Y-%m', 'now');"""
    
    cursor.execute(query, (user_id, category_id))
    result = cursor.fetchone()
    total_spent = result[0] if (result and result[0] is not None) else 0.0
    conn.close()

    return {
        "category_name": cat_name,
        "total_spent": total_spent,
        "budget_limit": budget_limit,
        "is_exceeded": total_spent > budget_limit
    }

import csv 

def export_expenses_to_csv(user_id, filename= "expense_report.csv"):

    expenses = get_user_expenses_detailed(user_id)

    if not expenses:
        print("\n No expenses found to export.")
        return False
    headers = ["Expenses ID", "Category", "Type", "Amount ($)", "Date", "Note"]

    try:
        with open(filename, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(headers)

            for exp in expenses:
                expense_id = exp[0]
                category_name = exp[1]
                trans_type = exp[2] if len(exp) > 2 else "expense"
                amount = exp[3] if len(exp) > 3 else 0.0
                date = exp[4] if len(exp) > 4 else ""
                note = exp[5] if len(exp) > 5 and exp[5] else ""

                writer.writerow([expense_id, category_name, trans_type, f"{amount:.2f}", date, note]) 

        print(f"\n Success! Detailed expenses exported to '{filename}'.")
        return True
    except Exception as e:
        print(f"\n Error exporting to CSV: {e}")
        return False
