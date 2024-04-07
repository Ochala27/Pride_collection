from flask import Flask, jsonify, request
from flask_mysqldb import MySQL

app = Flask(__name__)
@app.route('/')
def index():
    return "hello"
# MySQL configurations
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Ochala@27'
app.config['MYSQL_DB'] = 'pride_collection_db'

mysql = MySQL(app)

# Sample data for demonstration
sample_categories = ['Stationery', 'Drinkware', 'Accessories', 'Apparel', 'Special Occasion']
sample_offers = ['Birthday Offers', 'Seasonal Offers', 'Customized Offers']
sample_products = [
    {"id": 1, "category": "Stationery", "subcategory": "Personalized journals", "name": "Product 1", "price": 19.99},
    {"id": 2, "category": "Drinkware", "subcategory": "Water bottles", "name": "Product 2", "price": 24.99}
    # Add more sample products as needed
]

# Routes
@app.route('/categories', methods=['GET'])
def get_categories():
    return jsonify({'categories': sample_categories})

@app.route('/offers', methods=['GET'])
def get_offers():
    return jsonify({'offers': sample_offers})

@app.route('/products', methods=['GET'])
def get_products():
    # Fetch products from MySQL database
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM products")
    products = cur.fetchall()
    cur.close()
    return jsonify({'products': products})

@app.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    # Fetch product details from MySQL database
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM products WHERE id = %s", (product_id,))
    product = cur.fetchone()
    cur.close()
    return jsonify({'product': product})

@app.route('/products/new', methods=['POST'])
def add_product():
    # Add new product to MySQL database
    data = request.get_json()
    category = data['category']
    subcategory = data['subcategory']
    name = data['name']
    price = data['price']
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO products (category, subcategory, name, price) VALUES (%s, %s, %s, %s)",
                (category, subcategory, name, price))
    mysql.connection.commit()
    cur.close()
    return jsonify({'message': 'Product added successfully'})

@app.route('/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    # Update product details in MySQL database
    data = request.get_json()
    name = data['name']
    price = data['price']
    cur = mysql.connection.cursor()
    cur.execute("UPDATE products SET name = %s, price = %s WHERE id = %s", (name, price, product_id))
    mysql.connection.commit()
    cur.close()
    return jsonify({'message': 'Product updated successfully'})

@app.route('/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    # Delete product from MySQL database
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM products WHERE id = %s", (product_id,))
    mysql.connection.commit()
    cur.close()
    return jsonify({'message': 'Product deleted successfully'})

if __name__ == '__main__':
    app.run(debug=True)

