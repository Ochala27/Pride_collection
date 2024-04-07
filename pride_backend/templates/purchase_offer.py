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

@app.route('/purchase_offer', methods=['POST'])
def purchase_offer():
    if request.method == 'POST':
        name = request.form['name']
        order_type = request.form['order-type']
        date = request.form['date']
        description = request.form['description']

        # Save purchase offer to the database
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO purchase_offers (name, order_type, date, description) VALUES (%s, %s, %s, %s)", (name, order_type, date, description))
        mysql.connection.commit()
        cur.close()

        return redirect(url_for('view_orders'))

@app.route('/view_orders')
def view_orders():
    # Retrieve purchase offers from the database
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM purchase_offers")
    purchase_offers = cur.fetchall()
    cur.close()

    return render_template('view_orders.html', purchase_offers=purchase_offers)

if __name__ == '__main__':
    app.run(debug=True)

