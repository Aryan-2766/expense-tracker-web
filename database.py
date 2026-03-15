import sqlite3
from datetime import datetime
import os

class ExpenseTrackerDB:
    def __init__(self, db_name='expenses.db'):
        self.db_name = db_name
        self.init_db()

    def init_db(self):
        """Initialize the database and create tables if they don't exist."""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS expenses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    amount REAL NOT NULL,
                    description TEXT NOT NULL,
                    category TEXT NOT NULL,
                    date TEXT NOT NULL
                )
            ''')
            conn.commit()

    def add_expense(self, amount, description, category):
        """Add a new expense to the database."""
        date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO expenses (amount, description, category, date)
                VALUES (?, ?, ?, ?)
            ''', (amount, description, category, date))
            conn.commit()
            return cursor.lastrowid

    def get_all_expenses(self):
        """Retrieve all expenses from the database."""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM expenses ORDER BY date DESC')
            return cursor.fetchall()

    def get_expenses_by_category(self, category):
        """Retrieve expenses for a specific category."""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM expenses WHERE category = ? ORDER BY date DESC', (category,))
            return cursor.fetchall()

    def delete_expense(self, expense_id):
        """Delete an expense by its ID."""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM expenses WHERE id = ?', (expense_id,))
            conn.commit()
            return cursor.rowcount > 0

    def get_total_expenses(self):
        """Get the total amount of all expenses."""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT SUM(amount) FROM expenses')
            result = cursor.fetchone()[0]
            return result if result else 0.0

    def get_category_totals(self):
        """Get total expenses grouped by category."""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT category, SUM(amount) FROM expenses GROUP BY category ORDER BY SUM(amount) DESC')
            return cursor.fetchall()

    def get_expenses_in_date_range(self, start_date, end_date):
        """Get expenses within a date range."""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM expenses WHERE date BETWEEN ? AND ? ORDER BY date DESC',
                         (start_date, end_date))
            return cursor.fetchall()
