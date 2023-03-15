from flask import Blueprint
from flask import g
from flask import render_template
from flaskr.templates.auth.auth import login_required
from flaskr.db import get_db

bp = Blueprint("wos", __name__)


@bp.route("/")
def index():
    return render_template("index.html")


@bp.route("/dashboard")
@login_required
def dashboard():
    if g.user["account_type"] == "customer":
        return render_template("customer/dashboard.html")
    elif g.user["account_type"] == "delivery":
        return render_template("delivery/dashboard.html")
    elif g.user["account_type"] == "admin":
        return render_template("admin/dashboard.html")


@bp.route("/profile/<int:userid>")
def profile(userid):
    p = (
        get_db().execute("SELECT * FROM users WHERE id = ?", (userid,)).fetchone()
    )
    return render_template("profile.html", p=p)


@bp.route('/products')
def products():
    # Open a connection to the database

    # Retrieve the products from the databasel()
    p = (
        get_db().execute("SELECT * FROM products").fetchall()
    )

    # Render the products page with the retrieved products
    return render_template('products.html', products=p)
