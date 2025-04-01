from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate

db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()

# Configure login manager settings
login_manager.login_view = 'main.login'
login_manager.login_message_category = 'info'