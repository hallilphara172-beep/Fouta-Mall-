from flask import Flask, request, jsonify, render_template
import os

app = Flask(__name__)

users = []

products = [
    {"name": "Sac traditionnel", "price": 25},
    {"name": "Tissu Fouta", "price": 15}
]

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/register", methods=["POST"])
def register():
    data = request.json
    users.append(data)
    return jsonify({"message": "Utilisateur enregistré"})

@app.route("/add_product", methods=["POST"])
def add_product():
    data = request.json
    products.append(data)
    return jsonify({"message": "Produit ajouté"})

@app.route("/products", methods=["GET"])
def get_products():
    return jsonify(products)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
