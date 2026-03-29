import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager
from werkzeug.middleware.proxy_fix import ProxyFix
from app.config import config
from app.utils.logger import setup_logger

db = SQLAlchemy()
csrf = CSRFProtect()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'

def create_app(config_name: str | None = None) -> Flask:
    """
    Application Factory Pattern.
    Initializes Flask app, extensions, and logs.
    """
    if config_name is None:
        config_name = os.environ.get('FLASK_CONFIG', 'default')

    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # Initialize extensions
    db.init_app(app)
    csrf.init_app(app)
    login_manager.init_app(app)

    # Setup Logging
    setup_logger(app)

    # Wrap with ProxyFix if enabled
    if app.config.get('ENABLE_PROXY_FIX'):
        app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_port=1, x_prefix=1)

    with app.app_context():
        # Setup Login Manager Loader
        from app.models.user import User
        @login_manager.user_loader
        def load_user(user_id):
            return User.query.get(int(user_id))

        # Register Blueprints
        from app.blueprints.main import main_bp
        from app.blueprints.events import events_bp
        from app.blueprints.auth import auth_bp
        
        app.register_blueprint(main_bp)
        app.register_blueprint(events_bp, url_prefix='/events')
        app.register_blueprint(auth_bp, url_prefix='/auth')

        # Global Error Handlers
        from app.errors import register_error_handlers
        register_error_handlers(app)

        # Create tables (for first-run on Supabase/Local)
        db.create_all()

    return app
