#!/usr/bin/env python3
"""
Expense Tracker Web Application

A web-based expense tracking application built with Flask and SQLite.
"""

from flask import Flask, render_template, request, redirect, url_for, flash
from database import ExpenseTrackerDB
import os

app = Flask(__name__)
app.secret_key = 'expense_tracker_secret_key_2024'

# Initialize database
db = ExpenseTrackerDB()

@app.route('/')
def index():
    """Home page - show all expenses and summary."""
    expenses = db.get_all_expenses()
    total = db.get_total_expenses()
    category_totals = db.get_category_totals()
    return render_template('index.html', expenses=expenses, total=total, category_totals=category_totals)

@app.route('/add', methods=['GET', 'POST'])
def add_expense():
    """Add a new expense."""
    if request.method == 'POST':
        try:
            amount = float(request.form['amount'])
            description = request.form['description'].strip()
            category = request.form['category'].strip()

            if amount <= 0:
                flash('Amount must be positive.', 'error')
                return redirect(url_for('add_expense'))

            if not description:
                flash('Description is required.', 'error')
                return redirect(url_for('add_expense'))

            if not category:
                flash('Category is required.', 'error')
                return redirect(url_for('add_expense'))

            expense_id = db.add_expense(amount, description, category)
            flash(f'Expense added successfully!', 'success')
            return redirect(url_for('index'))

        except ValueError:
            flash('Invalid amount. Please enter a valid number.', 'error')
            return redirect(url_for('add_expense'))

    return render_template('add_expense.html')

@app.route('/delete/<int:expense_id>', methods=['POST'])
def delete_expense(expense_id):
    """Delete an expense by ID."""
    if db.delete_expense(expense_id):
        flash('Expense deleted successfully!', 'success')
    else:
        flash('Expense not found.', 'error')
    return redirect(url_for('index'))

@app.route('/category/<category>')
def category_expenses(category):
    """Show expenses for a specific category."""
    expenses = db.get_expenses_by_category(category)
    total = sum(expense[1] for expense in expenses)  # Sum amounts
    return render_template('category.html', expenses=expenses, category=category, total=total)

@app.route('/summary')
def summary():
    """Show expense summary."""
    total = db.get_total_expenses()
    category_totals = db.get_category_totals()
    return render_template('summary.html', total=total, category_totals=category_totals)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
