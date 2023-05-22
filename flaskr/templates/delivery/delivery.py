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
        get_db().execute("SELECT * FROM orders WHERE status = 'pending';").fetchall()
    )

    deliveries = (
        get_db().execute(
            "SELECT * FROM deliveries WHERE status = 'pending' AND worker_id = ?",
            (g.user["id"],)).fetchall()
    )
    # Render the products page with the retrieved products
    return render_template('delivery/orders.html', orders=orders, deliveries=deliveries)


@bp.route('/view/<int:order_id>', methods=['POST', 'GET'])
@login_required
@account_type_required('delivery')
def view():
    return


@bp.route('/take/<int:order_id>', methods=['POST', 'GET'])
@login_required
@account_type_required('delivery')
def take(order_id):
    db = get_db()
    db.execute(
        "UPDATE orders SET status = 'taken' WHERE id = ?",
        (order_id,),
    )
    db.execute(
        "INSERT INTO deliveries (worker_id,order_id) VALUES (?,?)",
        (g.user["id"], order_id),
    )
    db.commit()
    return redirect(request.referrer)
