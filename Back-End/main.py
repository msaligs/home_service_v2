from flask import Flask
from config import DevelopmentConfig
from application.model import StatusEnum, db, IST, User,Role, role_user, Location, Category, Professional, UserAddress
from application.model import Service, ServiceLocation, ServiceRequest, Payment, AssignRequest, ServiceReview, ProfessionalReview
from application.sec import datastore
from flask_security import Security
import flask_cors as cors
from flask_mail import Mail
from flask_restful import Api
from flask_migrate import Migrate
from flask_caching import Cache
from celery_tasks.celery_factory import celery_init_app
import flask_excel as excel


migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig)

    app.config['SECRET_KEY'] = "Some random generated key"
    app.config['BUNDLE_ERRORS'] = True

    cache = Cache(app)
    app.security = Security(app, datastore)

    db.init_app(app)
    migrate.init_app(app, db)
    api = Api(app)
    app.cache = cache

    excel.init_excel(app)

    cors.CORS(app)


    celery_app = celery_init_app(app)  
    # app.extensions["celery"] = celery_app


    with app.app_context():
        import application.views
        from celery_tasks.celery_schedule import celery_app
        import application.routes.user_routes as user_routes
        import application.routes.admin_routes as admin_routes
        import application.routes.professional_routes as professional_routes
        import application.routes.common_routes as common_routes
        import application.routes.celery_routes as celery_routes

        app.register_blueprint(user_routes.user_bp, url_prefix='/api/user')
        app.register_blueprint(admin_routes.admin_bp, url_prefix='/api/admin')
        app.register_blueprint(professional_routes.professional_bp, url_prefix='/api/professional')
        app.register_blueprint(common_routes.common_bp, url_prefix='/api/common')
        app.register_blueprint(celery_routes.celery_tasks_bp, url_prefix='/api/celery')


    return app, celery_app

app, celery_app = create_app()

# celery_app = celery_init_app(app)

if __name__ == '__main__':
    app.run(debug=True)
