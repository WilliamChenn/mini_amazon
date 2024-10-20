from flask import Flask
from flask_login import LoginManager
from .config import Config
from .db import DB

login = LoginManager()
login.login_view = 'users.login'

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    app.db = DB(app)
    login.init_app(app)

    from .index import bp as index_bp
    app.register_blueprint(index_bp)

    from .users import bp as user_bp
    app.register_blueprint(user_bp)
    
    from .social import bp as social_bp
    app.register_blueprint(social_bp)
    
    # Register the cart blueprint
    from .cart import bp as cart_bp
    app.register_blueprint(cart_bp)

    # Inside the create_app() function after registering other blueprints
    from .purchase import bp as purchase_bp
    app.register_blueprint(purchase_bp)


    return app
