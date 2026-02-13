from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

users = []
products = [
    {"name": "Sac traditionnel", "price": "25€"},
    {"name": "Tissu Fouta", "price": "15€"},
]

@app.route("/")
def home():
    return render_template("index.html", products=products)

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
    app.run()