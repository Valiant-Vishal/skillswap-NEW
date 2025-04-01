import os
from dotenv import load_dotenv

load_dotenv()

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    # Secret key for CSRF protection
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your_default_secret_key_here'  # Replace with a strong default key

    # SQLite database URL (default)
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'instance/skillswap.db')  # Database file location

    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Disables modification tracking

    # File upload configurations
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    UPLOAD_FOLDER = os.path.join(basedir, 'static/uploads')
