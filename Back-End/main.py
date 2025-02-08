from flask import Flask
from config import DevelopmentConfig
from application.model import db
from application.sec import datastore
from application.api import api
from application.resource import *
from flask_security import Security
import os
from flask_cors import CORS


def create_app(test_config=None):
    app = Flask(__name__)
    CORS(app)

    app.config.from_object(DevelopmentConfig)
    app.config['SECRET_KEY'] = ' msaligs Secret Key'
    app.security = Security(app, datastore)

    db.init_app(app)
    api.init_app(app)
    app.config['BUNDLE_ERRORS'] = True          # this will return all the errors of reqparser in a single response 

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass


    with app.app_context():
        import application.views

    
    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)