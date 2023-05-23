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


@bp.route('/myDeliveries')
@login_required
@account_type_required('delivery')
def myDeliveries():
    # Retrieve the products from the databasel()
    deliveries = (
        get_db().execute(
            "SELECT * FROM deliveries JOIN orders ON deliveries.order_id = orders.id WHERE NOT deliveries.status = 'pending' AND worker_id = ?",
            (g.user["id"],)).fetchall()
    )
    # Render the products page with the retrieved products
    return render_template('delivery/deliveries.html', deliveries=deliveries)


@bp.route('/viewOrder/<int:order_id>', methods=['POST', 'GET'])
@login_required
@account_type_required('delivery')
def viewOrder(order_id):
    order = (
        get_db().execute(
            "SELECT o.quantity, o.total_price,o.date_ordered,u.fname||' '||u.mname||' '||u.lname as fullname,ua.street||' '||ua.city||' '||ua.house_no as address,u.phone_number,p.* FROM orders as o JOIN users as u ON o.customer_id = u.id JOIN user_address as ua ON o.address = ua.id JOIN products as p ON o.product_id = p.id WHERE o.id = ?;",
            (order_id,)
        ).fetchone()
    )
    delivery = (
        get_db().execute(
            "SELECT * FROM deliveries WHERE order_id = ?;",
            (order_id,)
        ).fetchone()
    )
    return jsonify({'htmlresponse': render_template('delivery/delivery.html', order=order, delivery=delivery)})


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


@bp.route('/ordered/<int:delivery_id>', methods=['POST', 'GET'])
@login_required
@account_type_required('delivery')
def ordered(delivery_id):
    db = get_db()
    db.execute(
        "UPDATE deliveries SET status = 'delivered', date_delivered = datetime('now','localtime') WHERE id = ?",
        (delivery_id,),
    )
    db.commit()
    return redirect(url_for('delivery.orders'))

@bp.route('/cancel/<int:delivery_id>', methods=['POST', 'GET'])
@login_required
@account_type_required('delivery')
def cancel(delivery_id):
    db = get_db()
    db.execute(
        "UPDATE deliveries SET status = 'cancelled' WHERE id = ?",
        (delivery_id,),
    )
    db.commit()
    return redirect(url_for('delivery.orders'))
