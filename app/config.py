import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-key-please-change")
    SECURITY_PASSWORD_SALT = os.getenv("SECURITY_PASSWORD_SALT", "dev-salt")

    # Database Configuration
    # Render provides 'DATABASE_URL' starting with postgres:// which SQLAlchemy < 1.4 deprecated.
    # We must correct it to postgresql://
    uri = os.getenv("DATABASE_URL", "sqlite:///blog.db")
    if uri.startswith("postgres://"):
        uri = uri.replace("postgres://", "postgresql://", 1)

    SQLALCHEMY_DATABASE_URI = uri
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Mail Configuration
    MAIL_SERVER = os.getenv("MAIL_SERVER", "smtp.gmail.com")
    MAIL_PORT = int(os.getenv("MAIL_PORT", 465))
    MAIL_USE_TLS = os.getenv("MAIL_USE_TLS", "False").lower() == "false"
    MAIL_USE_SSL = os.getenv("MAIL_USE_SSL", "True").lower() == "true"
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = os.getenv("MAIL_USERNAME")
    MAIL_DEBUG = False
    MAIL_MAX_EMAILS = None
    MAIL_ASCII_ATTACHMENTS = False

    # CKEditor
    CKEDITOR_SERVE_LOCAL = True
    CKEDITOR_PKG_TYPE = "standard"
