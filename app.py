from flask import Flask, render_template_string, request, redirect, session

app = Flask(__name__)
app.secret_key = "secret123"

products = [
    {"id": 1, "name": "Chaussures Nike", "price": 15000,
     "image": "https://via.placeholder.com/150"},
    {"id": 2, "name": "Téléphone Samsung", "price": 120000,
     "image": "https://via.placeholder.com/150"},
    {"id": 3, "name": "Sac à main", "price": 20000,
     "image": "https://via.placeholder.com/150"},
]

HTML = """
<!DOCTYPE html>
<html>
<head>
<title>Fouta Mall</title>
<style>
body{font-family:Arial;background:#f5f5f5;margin:0}
header{background:orange;color:white;padding:15px;font-size:22px}
.container{padding:20px}
.grid{display:grid;grid-template-columns:repeat(3,1fr);gap:20px}
.card{background:white;padding:15px;border-radius:10px;text-align:center}
img{width:100%;border-radius:10px}
button{background:orange;color:white;border:none;padding:10px;margin-top:10px;border-radius:5px;cursor:pointer}
.cart{background:white;margin-top:30px;padding:20px;border-radius:10px}
.total{font-size:20px;margin-top:10px}
.remove{background:red}
</style>
</head>
<body>

<header>🛒 Fouta Mall</header>

<div class="container">

<h2>Produits</h2>

<div class="grid">
{% for p in products %}
<div class="card">
<img src="{{p.image}}">
<h3>{{p.name}}</h3>
<p>{{p.price}} FCFA</p>
<form method="POST" action="/add">
<input type="hidden" name="id" value="{{p.id}}">
<button>Ajouter au panier</button>
</form>
</div>
{% endfor %}
</div>

<div class="cart">
<h2>Panier</h2>

{% if cart %}
<ul>
{% for item in cart %}
<li>
{{item.name}} - {{item.price}} FCFA
<form method="POST" action="/remove" style="display:inline">
<input type="hidden" name="id" value="{{item.id}}">
<button class="remove">Supprimer</button>
</form>
</li>
{% endfor %}
</ul>

<p class="total">Total : {{total}} FCFA</p>

{% else %}
<p>Panier vide</p>
{% endif %}
</div>

</div>
</body>
</html>
"""

@app.route("/")
def home():
    cart = session.get("cart", [])
    total = sum(item["price"] for item in cart)
    return render_template_string(HTML, products=products, cart=cart, total=total)

@app.route("/add", methods=["POST"])
def add():
    pid = int(request.form["id"])
    cart = session.get("cart", [])
    for p in products:
        if p["id"] == pid:
            cart.append(p)
    session["cart"] = cart
    return redirect("/")

@app.route("/remove", methods=["POST"])
def remove():
    pid = int(request.form["id"])
    cart = session.get("cart", [])
    cart = [i for i in cart if i["id"] != pid]
    session["cart"] = cart
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)