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
    if 'delete' in request.form:
        product_id = request.form['productID']
        db = get_db()
        db.execute("DELETE FROM products WHERE id = ?", (product_id,))
        db.commit()
        flash("Deleted a Product!")
    elif 'save' in request.form:
        product_id = request.form['productID']
        product_name = request.form['name']
        product_description = request.form['description']
        product_price = request.form['price']
        q = "UPDATE products SET name=?, description=?, price=? WHERE id=?"
        cols = (product_name, product_description, product_price, product_id)
        if 'image' in request.files:
            image_file = request.files['image']
            if image_file.filename != '':
                # Save the file to a folder on the server
                filename = secure_filename(image_file.filename)
                image_file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
                # Update the query to include the filename
                q = "UPDATE products SET name=?, description=?, price=?, image_filename=? WHERE id=?"
                cols = (product_name, product_description, product_price, filename, product_id)
        db = get_db()
        db.execute(q, cols)
        db.commit()
        flash("Saved Product!")

    return redirect(url_for('wos.products'))
