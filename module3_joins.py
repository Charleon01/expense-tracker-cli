from db_helper import get_connection

def get_detailed_expenses(user_id):
    """Fetches expenses joined with category names for a specific user."""
    conn = get_connection()
    cursor = conn.cursor()
    
    query = """
    SELECT 
        e.expense_id,
        u.email,
        c.name AS category_name,
        c.type AS transaction_type,
        e.amount,
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

# Test the query
if __name__ == "__main__":
    expenses = get_detailed_expenses(1)
    print("--- Detailed Transaction History ---")
    for item in expenses:
        print(f"ID: {item[0]} | User: {item[1]} | Category: {item[2]} ({item[3]}) | Amount: ${item[4]} | Date: {item[5]}")