from application.api import *


api.add_resource(CategoryResource, '/categories', '/categories/<int:id>')

api.add_resource(LocationResource, '/locations', '/locations/<int:id>')

api.add_resource(UserResource, '/users')

api.add_resource(CategoriesByLocation, '/location/categories/<int:location_id>')