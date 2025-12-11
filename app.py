# app.py
import sqlite3
from flask import Flask, request, jsonify
import os

app = Flask(__name__)

DB_PATH = os.environ.get("DB_PATH", "/data/books.db")

# ---------------------------------------------------------
# Database connection
# ---------------------------------------------------------
def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# ---------------------------------------------------------
# Create table if not exists
# ---------------------------------------------------------
def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            year INTEGER NOT NULL
        );
    """)
    conn.commit()

init_db()

# ---------------------------------------------------------
# Routes API
# ---------------------------------------------------------

# GET ALL BOOKS
@app.route("/books", methods=["GET"])
def list_books():
    conn = get_db()
    rows = conn.execute("SELECT * FROM books").fetchall()
    return jsonify([dict(row) for row in rows])

# ADD A BOOK
@app.route("/books", methods=["POST"])
def add_book():
    data = request.json
    if not all(k in data for k in ("title", "author", "year")):
        return jsonify({"error": "Missing fields"}), 400

    conn = get_db()
    conn.execute(
        "INSERT INTO books (title, author, year) VALUES (?, ?, ?)",
        (data["title"], data["author"], data["year"])
    )
    conn.commit()
    return jsonify({"status": "book added"}), 201

# UPDATE BOOK
@app.route("/books/<int:book_id>", methods=["PUT"])
def update_book(book_id):
    data = request.json
    conn = get_db()
    conn.execute(
        "UPDATE books SET title=?, author=?, year=? WHERE id=?",
        (data["title"], data["author"], data["year"], book_id)
    )
    conn.commit()
    return jsonify({"status": "book updated"})

# DELETE BOOK
@app.route("/books/<int:book_id>", methods=["DELETE"])
def delete_book(book_id):
    conn = get_db()
    conn.execute("DELETE FROM books WHERE id=?", (book_id,))
    conn.commit()
    return jsonify({"status": "book deleted"})

# ---------------------------------------------------------
# Run server
# ---------------------------------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
