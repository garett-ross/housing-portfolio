from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

# Initialize SQLAlchemy as a global object
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///portfolio.db'
    # Initialize the db instance with the app
    db.init_app(app)
    CORS(app)

    # Register the blueprint
    from .utils import utils
    app.register_blueprint(utils)

    from .api import api
    app.register_blueprint(api)

    # Ensure database schema is created
    with app.app_context():
        db.create_all()

    @app.route("/")
    def hello():
        return "Hello"

    return app
