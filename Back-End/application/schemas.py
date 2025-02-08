from marshmallow import Schema, fields, validate
from application.model import User

class CategorySchema(Schema):
    id = fields.Int(dump_only=True)  # This field is only used for serialization (GET requests)
    name = fields.Str(required=True, validate=validate.Length(min=3))
    description = fields.Str(required=True, validate=validate.Length(min=10))
    image_url = fields.Str(validate=validate.URL())
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    active = fields.Bool()


class LocationSchema(Schema):
    id = fields.Int(dump_only=True)
    city = fields.Str(required=True, validate=validate.Length(min=5))
    state = fields.Str(required=True, validate=validate.Length(min=6))
    pincode = fields.Str(required=True, validate=validate.Length(min=6, max=6))
    created_at = fields.DateTime(dump_only=True)

class RoleSchema(Schema):
    name = fields.Str(required=True, validate=validate.OneOf(['user', 'professional']))

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=5))
    email = fields.Email(required=True)
    mobile = fields.Str(required=True, validate=validate.Length(min=10, max=10))
    password = fields.Str(load_only=True,required=True, validate=validate.Length(min=8))   # required for new user registration
    profile_img_url = fields.Str(validate=validate.URL())
    roles = fields.Method("get_first_role")
    # roles = fields.List(fields.Nested(RoleSchema)) 
    # roles = fields.List(fields.Str())
    active = fields.Bool()
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

    # def get_first_role(self, obj):
    #     if obj.roles:
    #         return obj.roles[0].name
    #     return None 
    def get_first_role(self, obj):
        if isinstance(obj, User):  # Check if obj is an instance of the User class
            print('yes')
            if obj.roles:
                return obj.roles[0].name
            return None
        elif isinstance(obj, str):  # Check if obj is a string
            print('no')
            return obj
        return None


class ServiceSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=5))
    description = fields.Str(required=True, validate=validate.Length(min=10))
    image_url = fields.Str(validate=validate.URL())
    category_id = fields.Int(required=True)
    time_required = fields.Int(required=True)
    base_price = fields.Float(required=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

class ProfessionalSchema(Schema):
    id = fields.Int(dump_only=True)
    user_id = fields.Int(required=True)
    category_id = fields.Int(required=True)
    location_id = fields.Int(required=True)
    rating = fields.Float()
    experience = fields.Float()
    available = fields.Bool()
    image_url = fields.Str(validate=validate.URL())
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)


