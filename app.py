from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# --- Database setup ---
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///products.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# --- Model ---
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "stock": self.stock
        }

# --- Routes ---
@app.route('/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    return jsonify([p.to_dict() for p in products])

@app.route('/products', methods=['POST'])
def add_product():
    data = request.get_json()
    name = data.get('name')
    price = float(data.get('price', 0))
    stock = int(data.get('stock', 0))

    if not name:
        return jsonify({"error": "Name is required"}), 400

    product = Product(name=name, price=price, stock=stock)
    db.session.add(product)
    db.session.commit()
    return jsonify(product.to_dict()), 201

if __name__ == '__main__':
    # Create tables and add demo products on first run
    with app.app_context():
        db.create_all()
        if Product.query.count() == 0:
            demo_products = [
                Product(name="Smartphone", price=19999, stock=10),
                Product(name="Laptop", price=54999, stock=5),
                Product(name="Wireless Earbuds", price=2999, stock=20)
            ]
            db.session.add_all(demo_products)
            db.session.commit()

    app.run(debug=True)
