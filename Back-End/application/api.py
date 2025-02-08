from flask import jsonify, request
from flask_security import auth_required, roles_required, roles_accepted, current_user,roles_accepted
from flask_restful import Resource, Api, reqparse
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from marshmallow import ValidationError
from application.model import *
from application.sec import datastore
from application.schemas import CategorySchema, LocationSchema,UserSchema
from datetime import datetime
from pytz import timezone
from werkzeug.security import generate_password_hash

api = Api(prefix='/api')
IST = timezone('Asia/Kolkata')


class UserResource(Resource):
    @auth_required('token')
    def get(self):
        if current_user.roles[0].name == 'admin':
            page = request.args.get('page', 1, type=int)
            per_page = request.args.get('per_page', 10, type=int)
            
            try:
                paginated_users = User.query.paginate(page=page, per_page=per_page, error_out=False)
                
                schema = UserSchema(exclude=("password",),many=True)
                users = schema.dump(paginated_users.items)

                # Return paginated data including pagination metadata
                return {
                    'users': users,  
                    'total_users': paginated_users.total,  # Total number of users
                    'total_pages': paginated_users.pages,  # Total number of pages
                    'current_page': paginated_users.page,  # Current page
                    'per_page': paginated_users.per_page,  # Number of users per page
                    "has_prev": paginated_users.has_prev,
                    "has_next": paginated_users.has_next

                }
            
            except Exception as e:
                return {'error': str(e)}, 500
        else:
            id = current_user.id
            try:
                user = User.query.get(id)
                schema = UserSchema(only=("name", "email", "mobile", "profile_img_url","roles", "created_at", "updated_at", ))
                dump = schema.dump(user)
                return jsonify(dump)
                # return {"user": dump, "role": role}
            except Exception as e:
                return {'error': str(e)}, 500
            


    def post(self):
        schema = UserSchema()
        data = request.json
        roles = data.pop('roles', None)

        try:
            data = schema.load(data)
        except ValidationError as err:
            return {'errors': err.messages}, 400

        if User.query.filter_by(email=data.get('email')).first():
            return {'error': 'User with this email already exists.'}, 400
        
        if User.query.filter_by(mobile=data.get('mobile')).first():
            return {'error': 'User with this mobile number already exists.'}, 400

        if 'password' in data:
                data['password'] = generate_password_hash(data['password'])

        user = datastore.create_user(**data,roles=[roles],active=False)
        try:
            db.session.commit()
            dump = schema.dump(user)
            return {"message": "User added successfully", "user": dump}, 201
        
        except IntegrityError as integrity_error:
            db.session.rollback()
            if "UNIQUE constraint" in str(integrity_error.orig):
                return {"error": "User with this email already exists."}, 400
            return {"error": "A database integrity error occurred."}, 400
        
        except SQLAlchemyError as db_error:
            db.session.rollback()
            return {'error': 'An error occurred while adding the new user. Please try again later.'}, 500
        
        except Exception as general_error:
            return {'error': 'An unexpected error occurred. Please try again later.'}, 500

    @auth_required('token')
    def put(self):
        schema = UserSchema(partial=True)  # Partial=True allows updating only some fields
        data = request.json
        if data.get('roles'):
            return {'error': 'Roles cannot be updated.'}
        else:
            data.pop('roles', None)

        try:
            data = schema.load(data)
        except ValidationError as err:
            return {'errors': err.messages}, 400
        id = current_user.id
        user = User.query.get(id)
        if not user:
            return {'error': 'User not found.'}, 404

        if data.get('email') or data.get('mobile'):
            return {'error': 'Email / Mobile cannot be updated.'}, 400
        

        for key, value in data.items():
            if key == 'password':
                user.password = generate_password_hash(value)
            else:
                setattr(user, key, value)
        user.updated_at = datetime.now(IST)
        try:
            db.session.commit()
            dump = schema.dump(user)
            return {"message": "User updated successfully", "user": dump}, 200
        
        except IntegrityError as integrity_error:
            db.session.rollback()
            if "UNIQUE constraint" in str(integrity_error.orig):
                return {"error": "User with this email already exists."}, 400
            return {"error": "A database integrity error occurred."}, 400
        
        except SQLAlchemyError as db_error:
            db.session.rollback()
            return {'error': 'An error occurred while updating the user. Please try again later.'}, 500
        
        except Exception as general_error:
            return {'error': 'An unexpected error occurred. Please try again later.'}, 500

        
    




class CategoryResource(Resource):
    def get(self, id=None):
        try:
            if id:
                category = Category.query.get(id)
                if not category:
                    return {'error': 'Category not found'}, 404
                categories = [category]
            else:
                categories = Category.query.all()

            # Determine schema based on user roles
            if current_user.is_authenticated:
                if current_user.roles[0].name == 'admin':
                    schema = CategorySchema(many=True)
                else:
                    schema = CategorySchema(exclude=("created_at", "updated_at", "active"), many=True)
            else:
                schema = CategorySchema(exclude=("created_at", "updated_at", "active"), many=True)

            dump = schema.dump(categories)
            return jsonify(dump)
        except Exception as e:
            return {'error': str(e)}, 500



    @auth_required('token')
    @roles_required('admin')
    def post(self):
        schema = CategorySchema()

        try:
            data = schema.load(request.json)
        except ValidationError as err:
            return {'errors': err.messages}, 400

        category = Category(**data)
        db.session.add(category)

        try:
            db.session.commit()
            dump = schema.dump(category)
            return {"message": "Category added successfully", "category": dump}, 201
        
        except IntegrityError as integrity_error:
            db.session.rollback()
            if "UNIQUE constraint" in str(integrity_error.orig):
                return {"error": "Category with this name already exists."}, 400
            return {"error": "A database integrity error occurred."}, 400
        
        except SQLAlchemyError as db_error:
            db.session.rollback()
            return {'error': 'An error occurred while adding the new category. Please try again later.'}, 500
        
        except Exception as general_error:
            return {'error': 'An unexpected error occurred. Please try again later.'}, 500



    @auth_required('token')
    @roles_required('admin')
    def put(self, id):
        schema = CategorySchema()

        try:
            data = schema.load(request.json)
        except ValidationError as err:
            return {'errors': err.messages}, 400

        category = Category.query.get(id)
        if category:
            category.name = data.get('name', category.name)
            category.description = data.get('description', category.description)
            category.image_url = data.get('image_url', category.image_url)
            category.updated_at = datetime.now(IST)
            
            try:
                db.session.commit()
                dump = schema.dump(category)
                return {"message": "Category updated successfully", "category": dump}
            
            except IntegrityError as integrity_error:
                db.session.rollback()
                if "UNIQUE constraint" in str(integrity_error.orig):
                    return {"error": "Category with this name already exists."}, 400
                return {"error": "A database integrity error occurred."}, 400
            
            except SQLAlchemyError as db_error:
                db.session.rollback()
                return {'error': 'An error occurred while updating the category. Please try again later.'}, 500
            
            except Exception as general_error:
                return {'error': 'An unexpected error occurred. Please try again later.'}, 500
        else:
            return {'error': 'Category not found'}, 404

    @auth_required('token')
    @roles_required('admin')
    def delete(self, id):
        category = Category.query.get(id)
        if category:
            db.session.delete(category)
            try:
                db.session.commit()
                return {"message": "Category deleted successfully"}
            except Exception as e:
                db.session.rollback()
                return {'error': 'An error occurred while deleting the category. Please try again later.'}, 500
        else:
            return {'error': 'Category not found'}, 404
        

# ---------------------------------------------------LocationResource---------------------------------------------------
class LocationResource(Resource):

    def get(self, id=None):
        # print("current_user")
        try:
            if id:
                location = Location.query.get(id)
                if not location:
                    return {'error': 'No Location found'}, 404
                locations = [location]
            else:
                locations = Location.query.all()

            # Determine schema based on user roles
            if current_user.is_authenticated:
                if current_user.roles[0].name == 'admin':
                    schema = LocationSchema(many=True)
                else:
                    schema = LocationSchema(exclude=(["created_at"]), many=True)
            else:
                schema = LocationSchema(exclude=(["created_at"]), many=True)

            dump = schema.dump(locations)
            return jsonify(dump)
        except Exception as e:
            return {'error': str(e)}, 500

    @auth_required('token')
    @roles_required('admin')
    def post(self):
        schema = LocationSchema()

        try:
            data = schema.load(request.json)
        except ValidationError as err:
            return {'errors': err.messages}, 400

        location = Location(**data)
        db.session.add(location)

        try:
            db.session.commit()
            dump = schema.dump(location)
            return {"message": "Location added successfully", "location": dump}, 201
        
        except IntegrityError as integrity_error:
            db.session.rollback()
            if "UNIQUE constraint" in str(integrity_error.orig):
                return {"error": "Location with this name already exists."}, 400
            return {"error": "A database integrity error occurred."}, 400
        
        except SQLAlchemyError as db_error:
            db.session.rollback()
            return {'error': 'An error occurred while adding the new location. Please try again later.'}, 500
        
        except Exception as general_error:
            return {'error': 'An unexpected error occurred. Please try again later.'}, 500

    @auth_required('token')
    @roles_required('admin')
    def put(self, id):
        schema = LocationSchema()

        try:
            data = schema.load(request.json)
        except ValidationError as err:
            return {'errors': err.messages}, 400

        location = Location.query.get(id)
        if location:
            location.city= data.get('city', location.city)
            location.state = data.get('state', location.state)
            location.pincode = data.get('pincode', location.pincode)

            try:
                db.session.commit()
                dump = schema.dump(location)
                return {"message": "Location updated successfully", "location": dump}
            except IntegrityError as integrity_error:
                db.session.rollback()
                if "UNIQUE constraint" in str(integrity_error.orig):
                    return {"error": "City or Pincode already exists."}, 400
                return {"error": "A database integrity error occurred."}, 400
            except SQLAlchemyError as db_error:
                db.session.rollback()
                return {'error': 'An error occurred while updating the location. Please try again later.'}, 500
            except Exception as general_error:
                return {'error': 'An unexpected error occurred. Please try again later.'}, 500
        else:
            return {'error': 'Location not found'}, 404
        
# ---------------------------------
class CategoriesByLocation(Resource):

    def get(self, location_id):
        print(location_id)
        # Fetch the location and its related categories
        location = Location.query.get(location_id)
        if not location:
            return {"message": "Location not found"}, 404

        # Use relationship to fetch categories
        categories = [
            {"id": sl.category.id, "name": sl.category.name,"description": sl.category.description, "image_url": sl.category.image_url}
            for sl in location.service_location
            if sl.active  # Only include active service locations
        ]

        return {
            "location": location.city,
            "categories": categories,
        }, 200


        


