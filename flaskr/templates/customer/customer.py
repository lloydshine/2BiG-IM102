from flask import Blueprint, jsonify
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

@bp.route('/order/<int:product_id>', methods=['POST', 'GET'])
@login_required
@account_type_required('customer')
def edit_product(product_id):
    p = (
        get_db().execute("SELECT * FROM products WHERE id = ?", (product_id,)).fetchone()
    )
    return jsonify({'htmlresponse': render_template('customer/order.html', p=p)})

