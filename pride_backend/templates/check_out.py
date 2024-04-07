from flask import Flask, render_template, request, jsonify, redirect, url_for
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

@app.route('/place_order', methods=['POST'])
def place_order():
    if request.method == 'POST':
        # Get order details from the form
        order_details = request.form['order_details']

        # Save order details to the database
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO orders (order_details) VALUES (%s)", (order_details,))
        mysql.connection.commit()
        cur.close()

        return redirect(url_for('view_orders'))

@app.route('/view_orders')
def view_orders():
    # Retrieve orders from the database
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM orders")
    orders = cur.fetchall()
    cur.close()

    return render_template('view_orders.html', orders=orders)

if __name__ == '__main__':
    app.run(debug=True)

