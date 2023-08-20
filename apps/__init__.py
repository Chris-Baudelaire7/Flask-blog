from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt  
from flask_login import LoginManager
from flask_mail import Mail
from apps.config import Config


db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
mail = Mail()

login_manager.login_view = "users.login"
login_manager.login_message_category = "warning"
login_manager.needs_refresh_message = "You must login to access this page"

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    
    with app.app_context():
        db.init_app(app)
        bcrypt.init_app(app)
        login_manager.init_app(app)
        mail.init_app(app)
        
        from apps.main.routes import main
        from apps.users.routes import users
        from apps.posts.routes import posts
        from apps.errors.handlers import errors

        app.register_blueprint(main)
        app.register_blueprint(users)
        app.register_blueprint(posts)
        app.register_blueprint(errors)
        
        return app