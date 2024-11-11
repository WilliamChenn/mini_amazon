# app/__init__.py

from flask import Flask
from flask_login import LoginManager
from .config import Config
from .db import DB

login = LoginManager()
login.login_view = 'users.login'  # Adjust based on your authentication setup

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize the database
    app.db = DB(app)

    # Initialize Flask-Login
    login.init_app(app)

    # Register Blueprints
    from .index import bp as index_bp
    app.register_blueprint(index_bp)

    from .users import bp as user_bp
    app.register_blueprint(user_bp)

    from .profile import bp as profile_bp
    app.register_blueprint(profile_bp)

    from .cart import bp as cart_bp
    app.register_blueprint(cart_bp)

    from .product import bp as products_bp
    app.register_blueprint(products_bp)

    # Register the 'seller' blueprint once
    from .inventory import bp as seller_bp
    app.register_blueprint(seller_bp)

    from .category import bp as categories_bp
    app.register_blueprint(categories_bp)

    return app
