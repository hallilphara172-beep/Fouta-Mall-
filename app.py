# app.py
from flask import Flask, render_template, request, redirect, session, url_for
import sqlite3

app = Flask(__name__)
app.secret_key = "secret123"


# ---------------- DATABASE ----------------
def init_db():
    conn = sqlite3.connect("store.db")
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS products(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        price REAL,
        image TEXT
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        password TEXT
    )
    """)

    conn.commit()
    conn.close()


@app.before_first_request
def setup():
    init_db()


# ---------------- HOME ----------------
@app.route("/")
def home():
    conn = sqlite3.connect("store.db")
    c = conn.cursor()
    c.execute("SELECT * FROM products")
    products = c.fetchall()
    conn.close()
    return render_template("index.html", products=products)


# ---------------- ADD PRODUCT ----------------
@app.route("/add", methods=["GET", "POST"])
def add_product():
    if request.method == "POST":
        name = request.form["name"]
        price = request.form["price"]
        image = request.form["image"]

        conn = sqlite3.connect("store.db")
        c = conn.cursor()
        c.execute("INSERT INTO products(name,price,image) VALUES(?,?,?)",
                  (name, price, image))
        conn.commit()
        conn.close()
        return redirect("/")

    return render_template("add.html")


# ---------------- CART ----------------
@app.route("/add_to_cart/<int:id>")
def add_to_cart(id):
    if "cart" not in session:
        session["cart"] = []

    cart = session["cart"]
    cart.append(id)
    session["cart"] = cart
    return redirect("/")


@app.route("/cart")
def cart():
    if "cart" not in session:
        return render_template("cart.html", products=[])

    ids = session["cart"]
    conn = sqlite3.connect("store.db")
    c = conn.cursor()

    products = []
    for i in ids:
        c.execute("SELECT * FROM products WHERE id=?", (i,))
        p = c.fetchone()
        if p:
            products.append(p)

    conn.close()
    return render_template("cart.html", products=products)


# ---------------- LOGIN ----------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect("store.db")
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username=? AND password=?",
                  (username, password))
        user = c.fetchone()
        conn.close()

        if user:
            session["user"] = username
            return redirect("/")
    return render_template("login.html")


# ---------------- REGISTER ----------------
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect("store.db")
        c = conn.cursor()
        c.execute("INSERT INTO users(username,password) VALUES(?,?)",
                  (username, password))
        conn.commit()
        conn.close()
        return redirect("/login")

    return render_template("register.html")


# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
