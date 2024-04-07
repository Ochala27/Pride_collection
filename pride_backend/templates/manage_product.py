from flask import Flask, render_template, request, jsonify
from flask_mysqldb import MySQL

app = Flask(__name__)

# MySQL configurations
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Ochala@27'
app.config['MYSQL_DB'] = 'pride_collection_db'

# Initialize MySQL
mysql = MySQL(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/products', methods=['GET'])
def get_products():
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM products")
        products = cur.fetchall()
        cur.close()

        return jsonify({"products": products}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/products/<int:id>', methods=['PUT', 'DELETE'])
def edit_or_delete_product(id):
    try:
        if request.method == 'PUT':
            category = request.form['category']
            subcategory = request.form['subcategory']
            name = request.form['product-name']
            price = request.form['product-price']

            cur = mysql.connection.cursor()
            cur.execute("UPDATE products SET category=%s, subcategory=%s, name=%s, price=%s WHERE id=%s", (category, subcategory, name, price, id))
            mysql.connection.commit()
            cur.close()

            return jsonify({"message": "Product updated successfully"}), 200
        elif request.method == 'DELETE':
            cur = mysql.connection.cursor()
            cur.execute("DELETE FROM products WHERE id=%s", (id,))
            mysql.connection.commit()
            cur.close()

            return jsonify({"message": "Product deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

