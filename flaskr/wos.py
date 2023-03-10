from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from werkzeug.exceptions import abort

from flaskr.auth import login_required
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
    return render_template("profile.html", p=p)
