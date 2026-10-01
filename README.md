#Interactive CLI Expense Tracker

A modular command-line application built with python and SQLite for managing personal finances, category tracking, budget alerting, and exporting financial reports. 

## Key Features 
* **Expense Logging: ** Quick menu-driven transaction entry mapped to specific categories.

* **Category Management: ** FULL CRUD support for spending and income categories.

* **Budgets Limits & Alerts: ** Real-time threshold alerts when monthly category spending exceeds target limits. 

* **SQL Aggregation & Analytics:** Time-based summaries (monthly trends, category breakdowns) powered by SQLite JOINS and 'strftime'.

* **CSV Data Exports:** one-click export of full transaction histories to '.csv' format.

## Tech Stack 

* **Lanuage: ** Python 3.x
* **Database: ** SQLite 3 ('sqlite3')
* **Libraries Used:** 'sys', 'csv' (Standard Library)

## Project Structure

'''text
expense-tracker/
|
|----app.py              # CLI Menu interface and interaction handlers
|----db_helpers.py       # SQLite queries, connection handling, and business Logic
|----tracker.db          # Local SQLite database file
|----expense_report.csv  # Exported CSV financial records 