from flask import Flask, render_template
from extensions import db, login_manager, migrate
from config import Config
from filters import time_ago  # Import the custom filter

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    
    # Register custom filters
    app.jinja_env.filters['time_ago'] = time_ago  # Register the time_ago filter
    
    # Configure login manager
    login_manager.login_view = 'main.login'
    login_manager.login_message_category = 'info'
    
    # Register blueprints
    from routes import main as main_blueprint
    app.register_blueprint(main_blueprint)
    
    # Error handlers
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404
    
    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('500.html'), 500
    
    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
