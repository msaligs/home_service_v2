from flask import Flask
from config import DevelopmentConfig
from application.model import db
from application.sec import datastore
from flask_security import Security
import flask_cors as cors
from flask_mail import Mail
from flask_restful import Api


def create_app():
    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig)

    app.config['SECRET_KEY'] = "Some random generated key"
    app.config['BUNDLE_ERRORS'] = True
    app.security = Security(app, datastore)

    db.init_app(app)

    api = Api(app)

    cors.CORS(app)
    with app.app_context():
        import application.views
        import application.routes.user_routes as user_routes
        import application.routes.admin_routes as admin_routes
        import application.routes.professional_routes as professional_routes
        import application.routes.common_routes as common_routes

        app.register_blueprint(user_routes.user_bp, url_prefix='/api/user')
        app.register_blueprint(admin_routes.admin_bp, url_prefix='/api/admin')
        app.register_blueprint(professional_routes.professional_bp, url_prefix='/api/professional')
        app.register_blueprint(common_routes.common_bp, url_prefix='/api/common')


    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
