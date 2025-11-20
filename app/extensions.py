from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail
from flask_login import LoginManager
from flask_caching import Cache
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)
migrate = Migrate()
mail = Mail()
cache = Cache(config={"CACHE_TYPE": "simple"})
limiter = Limiter(key_func=get_remote_address, storage_uri="memory://")

login_manager = LoginManager()
login_manager.login_view = "main.login" # type: ignore
login_manager.session_protection = "strong"


@login_manager.user_loader
def load_user(user_id):
    from .models import User

    return db.session.get(User, int(user_id))
