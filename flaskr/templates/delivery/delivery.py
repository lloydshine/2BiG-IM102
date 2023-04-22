from flask import Blueprint, jsonify, request, redirect, url_for
from flask import g
from flask import render_template
from flaskr.db import get_db
from flaskr.templates.auth.auth import account_type_required, login_required

bp = Blueprint("delivery", __name__)

@bp.route('/orders')
@login_required
@account_type_required('delivery')
def orders():
    # Retrieve the products from the databasel()
    orders = (
        get_db().execute("SELECT * FROM orders").fetchall()
    )
    # Render the products page with the retrieved products
    return render_template('delivery/orders.html', orders=orders)