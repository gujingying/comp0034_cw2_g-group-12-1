from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect

db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()
csrf._exempt_views.add('dash.dash.dispatch')
#csrf_protect = CSRFProtect()
#csrf_protect._exempt_views.add('dash.dash.dispatch')


def create_app(config_class_name):
    """
    Initialise the Flask application.
    :type config_class_name: Specifies the configuration class
    :rtype: Returns a configured Flask object
    """
    app = Flask(__name__)
    app.config.from_object(config_class_name)

    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)


    with app.app_context():
        # Import Dash application
        from dash_app.dash import init_dashboard
        app = init_dashboard(app)

    return app