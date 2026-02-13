from flask import Flask, request, jsonify

app = Flask(__name__)

users = []
products = []

@app.route("/")
def home():
    return "Bienvenue sur FOUTA MALL API"

@app.route("/register", methods=["POST"])
def register():
    data = request.json
    users.append(data)
    return jsonify({"message": "Utilisateur enregistré", "users": users})

@app.route("/add_product", methods=["POST"])
def add_product():
    data = request.json
    products.append(data)
    return jsonify({"message": "Produit ajouté", "products": products})

@app.route("/products", methods=["GET"])
def get_products():
    return jsonify(products)

if __name__ == "__main__":
    app.run()
