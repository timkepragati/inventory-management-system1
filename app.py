from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
import secrets

app = Flask(__name__)

# Generate a secure random key
app.secret_key = secrets.token_hex(16)  

# MySQL Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'pragatimke'
app.config['MYSQL_DB'] = 'inventory'

mysql = MySQL(app)

# Route for viewing products
@app.route('/')
def index():
    # Fetch data from the database
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM inventory')
    data = cur.fetchall()
    cur.close()
    return render_template('index.html', inventory=data)

# Route for adding a product
@app.route('/add', methods=['POST'])
def add():
    if request.method == 'POST':
        productname = request.form['productname']
        quantity = request.form['quantity']
        price = request.form['price']
        date = datetime.now().strftime('%Y-%m-%d')

        # Calculate the amount based on quantity and price
        amount = float(quantity) * float(price)

        # Insert data into the database
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO inventory (productname, quantity, price, amount, date) VALUES (%s, %s, %s, %s, %s)',
                    (productname, quantity, price, amount, date))
        mysql.connection.commit()
        cur.close()

        flash('Product added successfully', 'success')
        return redirect(url_for('index'))

# Route for updating a product
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    if request.method == 'POST':
        new_quantity = request.form['new_quantity']

        # Update data in the database
        cur = mysql.connection.cursor()
        cur.execute('UPDATE inventory SET quantity = %s WHERE id = %s', (new_quantity, id))
        mysql.connection.commit()
        cur.close()

        flash('Product updated successfully', 'success')
        return redirect(url_for('index'))
    else:
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM inventory WHERE id = %s', (id,))
        data = cur.fetchone()
        cur.close()

        return render_template('update.html', item=data)

# Route for deleting a product
@app.route('/delete/<int:id>')
def delete(id):
    # Delete data from the database
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM inventory WHERE id = %s', (id,))
    mysql.connection.commit()
    cur.close()

    flash('Product deleted successfully', 'success')
    return redirect(url_for('index'))

# Route for searching products
@app.route('/search', methods=['POST'])
def search():
    keyword = request.form['keyword']

    # Search for products in the database
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM inventory WHERE productname LIKE %s', ('%' + keyword + '%',))
    data = cur.fetchall()
    cur.close()

    return render_template('search.html', inventory=data)

if __name__ == '__main__':
    app.run(debug=True)
