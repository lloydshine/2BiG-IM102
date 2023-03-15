from flask import Blueprint
from flask import g
from flask import render_template
from flaskr.templates.auth.auth import customer_required
from flaskr.db import get_db

bp = Blueprint("customer", __name__)

@bp.route('/myorders')
@customer_required
def myorders():
    # Open a connection to the database

    # Retrieve the products from the databasel()
    orders = (
        get_db().execute("SELECT * FROM orders WHERE customer_id = ?", (g.user["id"],)).fetchall()
    )

    # Render the products page with the retrieved products
    return render_template('customer/myorders.html', orders=orders)
