from flask import Blueprint, url_for, redirect, request
from flask import g
from flask import render_template
from flaskr.templates.auth.auth import login_required
from flaskr.db import get_db

bp = Blueprint("wos", __name__)


@bp.route("/")
def index():
    return render_template("index.html")


@bp.route("/profile/<int:userid>")
def profile(userid):
    p = (
        get_db().execute("SELECT * FROM users WHERE id = ?", (userid,)).fetchone()
    )
    a = (
        get_db().execute("SELECT * FROM user_address WHERE user_id = ?", (userid,)).fetchall()
    )
    return render_template("profile.html", p=p,a=a)

@bp.route("/updateProfile/<int:userid>",methods=['POST', 'GET'])
@login_required
def updateProfile(userid):
    fname = request.form['fname']
    mname = request.form['mname']
    lname = request.form['lname']
    username = request.form['username']
    password = request.form['password']
    phoneno = request.form['phone']

    db = get_db()
    db.execute(
        "UPDATE users SET fname=?,mname=?,lname=?,username=?,password=?,phone_number=? WHERE id = ?",
        (fname,lname,mname,username,password,phoneno,userid),
    )
    db.commit()
    return redirect(url_for('wos.profile', userid=userid))

@bp.route("/add_address", methods=['POST', 'GET'])
@login_required
def addAddress():
    # get the form
    street = request.form['street']
    houseno = request.form['houseno']
    city = request.form['city']
    # insert the order to address table
    db = get_db()
    db.execute(
        "INSERT INTO user_address (user_id,street,house_no,city) VALUES (?,?,?,?)",
        (g.user["id"],street,houseno,city),
    )
    db.commit()
    # return to products page
    return redirect(url_for('wos.profile', userid=g.user["id"]))

@bp.route("/delete_address/<int:addressid>",methods=['POST'])
@login_required
def deleteAddress(addressid):
    db = get_db()
    db.execute(
        "DELETE FROM user_address WHERE id = ?",
        (addressid,)
    )
    db.commit()
    return redirect(url_for('wos.profile', userid=g.user["id"]))

@bp.route('/products')
def products():
    # Open a connection to the database

    # Retrieve the products from the databasel()
    p = (
        get_db().execute("SELECT * FROM products").fetchall()
    )

    # Render the products page with the retrieved products
    return render_template('products.html', products=p)
