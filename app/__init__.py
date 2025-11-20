from flask import Flask
from flask_bootstrap import Bootstrap5
from flask_ckeditor import CKEditor
from flask_wtf.csrf import CSRFProtect
from .config import Config
from .extensions import db, migrate, mail, login_manager, cache, limiter


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize Extensions
    db.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)
    Bootstrap5(app)
    CKEditor(app)
    csrf = CSRFProtect(app)
    login_manager.init_app(app)
    cache.init_app(app)
    limiter.init_app(app)

    # Import Models to ensure they are registered with SQLAlchemy
    from .models import User, BlogPost, Comment, ContactSubmission

    # Register Blueprints/Routes
    from .routes import main_bp

    app.register_blueprint(main_bp)

    # Global Context Processors
    from datetime import datetime
    from flask_login import current_user

    @app.context_processor
    def inject_globals():
        gravatar = None
        if current_user.is_authenticated:
            gravatar = current_user.avatar(30)
        return dict(gravatar=gravatar, now=datetime.now())

    return app
