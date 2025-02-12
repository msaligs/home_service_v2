from flask import Flask
from config import DevelopmentConfig
from application.model import db
from application.sec import datastore
from flask_security import Security


def create_app():
    app = Flask(__name__)

    app.config.from_object(DevelopmentConfig)
    app.config['SECRET_KEY'] = "Some random generated key"
    app.config['BUNDLE_ERRORS'] = True
    app.security = Security(app, datastore)

    db.init_app(app)
    with app.app_context():
        import application.views
    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
