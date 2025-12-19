from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)

BOOKS_FILE = "books.json"

# Hardcoded admin credentials
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "1234"

# ---------------- Helper Functions ----------------
def load_books():
    if not os.path.exists(BOOKS_FILE):
        with open(BOOKS_FILE, "w") as f:
            json.dump([], f)
    with open(BOOKS_FILE, "r") as f:
        return json.load(f)

def save_books(books):
    with open(BOOKS_FILE, "w") as f:
        json.dump(books, f, indent=4)

# ---------------- Admin Login ----------------
@app.route("/admin/login", methods=["POST"])
def admin_login():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
        return jsonify({"success": True})
    else:
        return jsonify({"success": False})

# ---------------- Admin Endpoints ----------------
@app.route("/admin/books", methods=["GET"])
def get_admin_books():
    books = load_books()
    return jsonify(books)

@app.route("/admin/books", methods=["POST"])
def add_book():
    data = request.json
    books = load_books()
    book = {"title": data["title"], "author": data["author"], "available": True}
    books.append(book)
    save_books(books)
    return jsonify({"message": "Book added successfully"})

@app.route("/admin/books/<int:index>", methods=["DELETE"])
def delete_book(index):
    books = load_books()
    if 0 <= index < len(books):
        books.pop(index)
        save_books(books)
        return jsonify({"message": "Book deleted successfully"})
    return jsonify({"message": "Invalid index"})

# ---------------- User Endpoints ----------------
@app.route("/books", methods=["GET"])
def get_books():
    books = load_books()
    return jsonify(books)

@app.route("/books/<int:index>/borrow", methods=["POST"])
def borrow_book(index):
    books = load_books()
    if 0 <= index < len(books):
        if books[index]["available"]:
            books[index]["available"] = False
            save_books(books)
            return jsonify({"message": "Book borrowed successfully"})
        else:
            return jsonify({"message": "Book already borrowed"})
    return jsonify({"message": "Invalid index"})

@app.route("/books/<int:index>/return", methods=["POST"])
def return_book(index):
    books = load_books()
    if 0 <= index < len(books):
        if not books[index]["available"]:
            books[index]["available"] = True
            save_books(books)
            return jsonify({"message": "Book returned successfully"})
        else:
            return jsonify({"message": "Book is already available"})
    return jsonify({"message": "Invalid index"})

if __name__ == "__main__":
    app.run(debug=True)
