from flask import Flask, render_template, session, redirect, url_for, request
import os

app = Flask(__name__)
app.secret_key = "fouta_secret_key"

# Produits fictifs
products = [
    {"id": 1, "name": "Fouta Traditionnelle", "price": 25, "image": "fouta1.jpg"},
    {"id": 2, "name": "Fouta Luxe", "price": 40, "image": "fouta2.jpg"},
    {"id": 3, "name": "Fouta Premium", "price": 60, "image": "fouta3.jpg"}
]

@app.route('/')
def home():
    return render_template("index.html", products=products)

@app.route('/products')
def product_page():
    return render_template("products.html", products=products)

@app.route('/add_to_cart/<int:id>')
def add_to_cart(id):
    if "cart" not in session:
        session["cart"] = []

    session["cart"].append(id)
    session.modified = True
    return redirect(url_for("cart"))

@app.route('/cart')
def cart():
    if "cart" not in session:
        session["cart"] = []

    cart_products = [p for p in products if p["id"] in session["cart"]]
    total = sum(p["price"] for p in cart_products)

    return render_template("cart.html", cart_products=cart_products, total=total)

if __name__ == "__main__":
    app.run(debug=True)
