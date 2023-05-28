from flask import Blueprint, jsonify
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask import current_app
from werkzeug.utils import secure_filename
import os
from flaskr.db import get_db
from flaskr.templates.auth.auth import account_type_required, login_required

bp = Blueprint("admin", __name__)

ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif'}


# Function to check if file extension is allowed
def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@bp.route('/add_product', methods=['POST', 'GET'])
@login_required
@account_type_required('admin')
def add_product():
    if request.method == 'POST':
        product_name = request.form['name']
        product_description = request.form['description']
        product_price = request.form['price']
        image_file = request.files['image']

        # Check if the image file is allowed
        if image_file and allowed_file(image_file.filename):
            # Save the image file to the server
            filename = secure_filename(image_file.filename)
            image_file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))

            # Save the product to the database
            db = get_db()
            db.execute('INSERT INTO products (name, description, price, image_filename) VALUES (?, ?, ?, ?)',
                       (product_name, product_description, product_price, filename))
            db.commit()
            applog = "Added new product"
            flash(applog)
            return redirect(url_for('wos.products'))
    # Render the add product form if the request method is not POST or the image file is not allowed
    return render_template('admin/add_product.html')


@bp.route('/edit_product/<int:product_id>', methods=['POST', 'GET'])
@login_required
@account_type_required('admin')
def edit_product(product_id):
    p = (
        get_db().execute("SELECT * FROM products WHERE id = ?", (product_id,)).fetchone()
    )
    return jsonify({'htmlresponse': render_template('admin/edit_product.html', p=p)})


@bp.route('/product', methods=['POST'])
@login_required
@account_type_required('admin')
def product():
    product_id = request.form['productID']
    db = get_db()

    if 'delete' in request.form:
        # Get the product image file name from database
        image_filename = db.execute("SELECT image_filename FROM products WHERE id=?", (product_id,)).fetchone()[0]

        # Delete the image file from the static/uploads folder
        os.remove(os.path.join(current_app.config['UPLOAD_FOLDER'], image_filename))
        db.execute("DELETE FROM products WHERE id = ?", (product_id,))
        flash("Deleted a Product!")
    elif 'save' in request.form:
        product_name, product_description, product_price = request.form['name'], request.form['description'], \
            request.form['price']
        q, cols = "UPDATE products SET name=?, description=?, price=?", (
            product_name, product_description, product_price)

        if 'image' in request.files:
            image_file = request.files['image']
            if image_file.filename != '':
                # Save the file to a folder on the server
                filename = secure_filename(image_file.filename)
                image_file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
                q, cols = "UPDATE products SET name=?, description=?, price=?, image_filename=?", (
                    product_name, product_description, product_price, filename)

        db.execute(q + " WHERE id=?", cols + (product_id,))
        flash("Edited Product!")

    db.commit()
    return redirect(url_for('wos.products'))


@bp.route('/logs', methods=['POST', 'GET'])
@login_required
@account_type_required('admin')
def logs():
    orders = (
        get_db().execute("SELECT * FROM orders").fetchall()
    )
    return render_template('admin/orddel.html', orders=orders)

@bp.route('/viewOrdel/<int:order_id>', methods=['POST', 'GET'])
@login_required
@account_type_required('admin')
def viewOrdel(order_id):
    order = (
        get_db().execute(
            "SELECT o.status,o.quantity,o.total_price,o.date_ordered,u.fname||' '||u.mname||' '||u.lname as fullname,ua.street||' '||ua.city||' '||ua.house_no as address,u.phone_number,p.* FROM orders as o JOIN users as u ON o.customer_id = u.id JOIN user_address as ua ON o.address = ua.id JOIN products as p ON o.product_id = p.id WHERE o.id = ?;",
            (order_id,)
        ).fetchone()
    )
    delivery = None
    if order['status'] != 'pending':
        delivery = get_db().execute(
            "SELECT * FROM deliveries JOIN users ON deliveries.worker_id = users.id WHERE order_id = ?",
            (order_id,),
        ).fetchone()
    return jsonify({'htmlresponse': render_template('admin/view_ordel.html', order=order, delivery=delivery)})

@bp.route("/adminDashboard")
@login_required
@account_type_required('admin')
def dashboard():
    summ = (
        get_db().execute('''
        SELECT 
  (
    SELECT SUM(quantity)
    FROM orders
    WHERE orders.id IN (
      SELECT order_id
      FROM deliveries
      WHERE deliveries.status = 'delivered'
    )
  ) AS total_sold_products,
    (
    SELECT SUM(total_price)
    FROM orders
    WHERE orders.id IN (
      SELECT order_id
      FROM deliveries
      WHERE deliveries.status = 'delivered'
    )
  ) AS total_income,
    (
    SELECT COUNT(*)
    FROM orders
  ) AS total_orders;
        ''').fetchone()
    )

    products = get_db().execute('''
    SELECT 
    p.id AS product_id,
    p.name AS product_name,
    COUNT(o.id) AS total_orders
FROM 
    products p
LEFT JOIN 
    orders o ON p.id = o.product_id
GROUP BY 
    p.id, p.name
ORDER BY 
    total_orders DESC;
    ''')

    top_workers = get_db().execute('''
    SELECT
  d.worker_id,
  u.fname AS worker_name,
  COUNT(d.id) AS total_deliveries
FROM
  deliveries d
JOIN
  users u ON d.worker_id = u.id
GROUP BY
  d.worker_id, u.fname
ORDER BY
  total_deliveries DESC;
    ''')

    workers = get_db().execute('''
        SELECT * FROM users WHERE account_type = 'delivery'
        ''').fetchall()

    return render_template("admin/dashboard.html", summ=summ, products=products, top=top_workers, workers=workers)

@bp.route('/add_worker', methods=['POST', 'GET'])
@login_required
@account_type_required('admin')
def add_worker():
    if request.method == 'POST':
        fname = request.form['fname']
        mname = request.form['mname']
        lname = request.form['lname']
        username = request.form['username']
        password = request.form['password']
        phone_number = request.form['phone']

        db = get_db()
        db.execute(
            "INSERT INTO users (fname,mname,lname,username,password,phone_number,account_type) VALUES (?,?,?,?,?,?,'delivery')",
            (fname, lname, mname, username, password, phone_number),
        )
        db.commit()
        return redirect(url_for('admin.dashboard'))
    return render_template('admin/add_worker.html')

@bp.route('/remove_worker/<int:worker_id>', methods=['POST', 'GET'])
@login_required
@account_type_required('admin')
def remove_worker(worker_id):
    db = get_db()
    db.execute(
        "DELETE FROM users WHERE id = ?",
        (worker_id,)
    )
    db.execute(
        "DELETE FROM deliveries WHERE worker_id = ?",
        (worker_id,)
    )
    db.commit()
    return redirect(url_for('admin.dashboard'))