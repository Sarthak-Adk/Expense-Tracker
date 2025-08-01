from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime

app = Flask(__name__)
DB = 'expense.db'

# Initialize DB
def init_db():
    with sqlite3.connect(DB) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                amount REAL NOT NULL,
                category TEXT NOT NULL,
                date TEXT NOT NULL
            )
        """)
init_db()

# Home page: view + add
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        amount = float(request.form["amount"])
        category = request.form["category"]
        date = request.form["date"] or datetime.now().strftime("%Y-%m-%d")
        with sqlite3.connect(DB) as conn:
            conn.execute("INSERT INTO expenses (amount, category, date) VALUES (?, ?, ?)", (amount, category, date))
        return redirect(url_for("index"))

    with sqlite3.connect(DB) as conn:
        expenses = conn.execute("SELECT * FROM expenses ORDER BY date DESC").fetchall()
        total = conn.execute("SELECT SUM(amount) FROM expenses").fetchone()[0] or 0

    return render_template("index.html", expenses=expenses, total=total)

# Delete
@app.route("/delete/<int:expense_id>")
def delete(expense_id):
    with sqlite3.connect(DB) as conn:
        conn.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
