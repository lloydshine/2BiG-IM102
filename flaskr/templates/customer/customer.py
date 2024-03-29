from flask import Blueprint, jsonify, request, redirect, url_for
from flask import g
from flask import render_template
from flaskr.db import get_db
from flaskr.templates.auth.auth import account_type_required, login_required

bp = Blueprint("customer", __name__)

@bp.route('/myorders')
@login_required
@account_type_required('customer')
def myorders():
    # Open a connection to the database

    # Retrieve the products from the databasel()
    orders = (
        get_db().execute("SELECT * FROM orders WHERE customer_id = ?", (g.user["id"],)).fetchall()
    )

    # Render the products page with the retrieved products
    return render_template('customer/myorders.html', orders=orders)

@bp.route('/customerOrder/<int:product_id>', methods=['POST', 'GET'])
@login_required
@account_type_required('customer')
def order(product_id):
    p = (
        get_db().execute("SELECT * FROM products WHERE id = ?", (product_id,)).fetchone()
    )
    return jsonify({'htmlresponse': render_template('customer/order.html', p=p)})


@bp.route('/placeorder/<int:product_id>', methods=['POST', 'GET'])
@login_required
@account_type_required('customer')
def place_order(product_id):
    #get the form
    address = request.form['address']
    quantity = request.form['quantity']
    total_price = request.form['total_price']
    #insert the order to oders table
    db = get_db()
    db.execute(
        "INSERT INTO orders (customer_id, product_id,address,quantity, total_price) VALUES (?, ?, ?,?, ?)",
        (g.user["id"], product_id,address, quantity, total_price),
    )
    db.commit()
    #return to products page
    return redirect(url_for('wos.products'))


@bp.route('/cancelorder/<int:order_id>', methods=['POST', 'GET'])
@login_required
@account_type_required('customer')
def cancel_order(order_id):
    db = get_db()
    db.execute(
        "UPDATE orders SET status = 'cancelled' WHERE id = ?",
        (order_id,)
    )
    db.commit()
    return redirect(url_for('customer.myorders'))

@bp.route('/viewmyorder/<int:order_id>', methods=['POST', 'GET'])
@login_required
@account_type_required('customer')
def view_order(order_id):
    db = get_db()
    order = (
        get_db().execute("SELECT * FROM orders WHERE id = ?", (order_id,)).fetchone()
    )
    product = (
        get_db().execute("SELECT * FROM products WHERE id = ?", (order['product_id'],)).fetchone()
    )
    delivery = None
    if order['status'] != 'pending':
        delivery = db.execute(
            "SELECT * FROM deliveries JOIN users ON deliveries.worker_id = users.id WHERE order_id = ?",
            (order_id,),
        ).fetchone()

    return jsonify({'htmlresponse': render_template('customer/myorder.html', order=order,delivery=delivery,product=product)})

