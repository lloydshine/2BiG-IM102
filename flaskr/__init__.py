import os
from flask import Flask
#flask --app flaskr --debug run
#flask --app flaskr init-db

def create_app(test_config=None):
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        # a default secret that should be overridden by instance config
        SECRET_KEY="dev",
        # store the database in the instance folder
        DATABASE=os.path.join(app.instance_path, "flaskr.sqlite"),
        UPLOAD_FOLDER=os.path.join(app.static_folder, 'uploads'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.update(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route("/hello")
    def hello():
        return "Hello, World!"

    # register the database commands
    from flaskr import db

    db.init_app(app)

    # apply the blueprints to the app
    from flaskr import wos
    from flaskr.templates.auth import auth
    from flaskr.templates.admin import admin
    from flaskr.templates.customer import customer
    from flaskr.templates.delivery import delivery

    app.register_blueprint(auth.bp)
    app.register_blueprint(wos.bp)
    app.register_blueprint(admin.bp)
    app.register_blueprint(customer.bp)
    app.register_blueprint(delivery.bp)


    app.add_url_rule("/", endpoint="index")

    return app
