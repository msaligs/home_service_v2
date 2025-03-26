from flask_sqlalchemy import SQLAlchemy
from flask_security import UserMixin, RoleMixin
from pytz import timezone
from sqlalchemy import CheckConstraint
from datetime import datetime
from sqlalchemy.orm import validates
from sqlalchemy import Enum as SAEnum
from enum import Enum

class StatusEnum(str, Enum):
    PENDING = 'pending'
    ASSIGNED = 'assigned'
    ACCEPTED = 'accepted'
    VERIFIED = 'verified'
    REJECTED = 'rejected'
    COMPLETED = 'completed'
    CANCELLED = 'cancelled'
    FAILED = 'failed'
    PAID = 'paid'



db = SQLAlchemy()

IST = timezone('Asia/Kolkata')

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)   
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    mobile = db.Column(db.String(10),unique=True, nullable=False)

    profile_img_url = db.Column(db.String(120), nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(IST))    
    updated_at = db.Column(db.DateTime, nullable=True)
    active = db.Column(db.Boolean)  # db default not work for datastore user
    
    fs_uniquifier = db.Column(db.String(255), unique=True)
    roles = db.relationship('Role', secondary='role_user', backref=db.backref('users', lazy='dynamic'))

    # __table_args__ = (
    #     CheckConstraint('length(mobile) = 10', name='check_mobile_length'),  # EXACT 10 characters 
    # )

    @validates('mobile')
    def validate_mobile(self, key, value):
        if not value.isdigit() or len(value) != 10:
            raise ValueError("Mobile number must be exactly 10 digits")
        return value

    def __repr__(self):
        return '<User %r>' % self.name
    
    def get_id(self):
        return str(self.id)


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    description = db.Column(db.String(120), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(IST))
    

role_user = db.Table('role_user',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer, db.ForeignKey('role.id'))
)


class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(120), nullable=False,unique=True)
    state = db.Column(db.String(120), nullable=False)
    # pincode = db.Column(db.String(120), nullable=False, unique=True)
    # created_at = db.Column(db.DateTime, default=datetime.now(IST))
    active = db.Column(db.Boolean,default=True)
    
    def __repr__(self):
        return f"<Location {self.city}, {self.state}>"


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    description = db.Column(db.String(120), nullable=False)
    image_url = db.Column(db.String(120), nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(IST))
    updated_at = db.Column(db.DateTime, nullable=True)
    active = db.Column(db.Boolean, default=True)
    
    def __repr__(self):
        return '<Category %r>' % self.name
    

class Professional(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    location_id = db.Column(db.Integer, db.ForeignKey('location.id'), nullable=False)
    
    rating = db.Column(db.Float, nullable=True, default=5)
    experience = db.Column(db.Float, nullable=True)
    available = db.Column(db.Boolean, default=True)
    # image_url = db.Column(db.String(120), nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(IST))
    updated_at = db.Column(db.DateTime, nullable=True)
    status = db.Column(db.String(20), default="pending")  # 'pending', 'verified', or 'rejected'
    status_updated_at = db.Column(db.DateTime, nullable= True)
    remarks = db.Column(db.String(150))
    # Define relationships
    category = db.relationship('Category', backref='professionals', lazy='joined')
    location = db.relationship('Location', backref='professionals', lazy='joined')
    user = db.relationship('User', uselist=False, backref='professional')

    def __repr__(self):
        return f"<Professional {self.id}>"


# to store user addresses to provide service --> one-to-many relationship with user
class UserAddress(db.Model):
    __tablename__ = 'user_address'
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    address = db.Column(db.String(120), nullable=False)
    # city = db.Column(db.String(120), nullable=False)
    # state = db.Column(db.String(120), nullable=False)
    location_id = db.Column(db.Integer, db.ForeignKey('location.id'), nullable=False)
    pincode = db.Column(db.String(120), nullable=False)

    user = db.relationship('User', backref='user_address', lazy='joined')
    location = db.relationship('Location', backref='user_address', lazy='joined')

    created_at = db.Column(db.DateTime, default=lambda: datetime.now(IST))
    updated_at = db.Column(db.DateTime, nullable=True)
    


class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(120), nullable=False)
    image_url = db.Column(db.String(120), nullable=True)

    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)

    # time_required = db.Column(db.Integer, nullable=False )   # time required in minutes
    base_price = db.Column(db.Float, nullable=False)        # price in INR   
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(IST))
    updated_at = db.Column(db.DateTime, nullable=True)
    active = db.Column(db.Boolean, default=True)

    category = db.relationship('Category', backref=db.backref('services', lazy='dynamic'))
    
    __table_args__ = (
        CheckConstraint('base_price >= 10 AND base_price <= 1000', name='check_price_positive'),
    )
    def __repr__(self):
        return '<Service %r>' % self.name



# for many-to-many relationship between location and category --> product of #locations and #categories
class ServiceLocation(db.Model):
    __tablename__ = 'service_location'
    id = db.Column(db.Integer, primary_key=True)

    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    # location_id = db.Column(db.String(120), db.ForeignKey('location.id'), nullable=False)
    location_id = db.Column(db.Integer, db.ForeignKey('location.id'), nullable=False)

    # surcharge = db.Column(db.Float, nullable=False, default=0)
    active = db.Column(db.Boolean, default=True)

    created_at = db.Column(db.DateTime, default=lambda: datetime.now(IST))
    updated_at = db.Column(db.DateTime, nullable=True)

    category = db.relationship('Category', backref=db.backref('service_location'))
    location = db.relationship('Location', backref=db.backref('service_location'))


class ServiceRequest(db.Model):
    __tablename__ = 'service_request'
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'), nullable=False)
    professional_id = db.Column(db.Integer, db.ForeignKey('professional.id'), nullable=True)    #nullable if request is pending ,   after request is accepted, this field will be updated with professional_id
    location_id = db.Column(db.Integer, db.ForeignKey('location.id'), nullable=False)

    status = db.Column(db.Enum(StatusEnum), nullable=False, default=StatusEnum.PENDING)       #current status of the request --> pending, accepted, completed, cancelled
    request_date = db.Column(db.DateTime, nullable = False, default=lambda: datetime.now(IST))
    completition_date = db.Column(db.DateTime, nullable=True)

    total_price = db.Column(db.Float, nullable=False,default=0)
    remarks = db.Column(db.String(120), nullable=True)

    service = db.relationship('Service', backref='service_requests', lazy='joined')
    locaation = db.relationship('Location', backref='service_requests', lazy='joined')
    user = db.relationship('User', backref='service_requests', lazy='joined')
    professional = db.relationship('Professional', backref='service_requests', lazy='joined')



class AssignRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    service_request_id = db.Column(db.Integer, db.ForeignKey('service_request.id'), nullable=False)
    professional_id = db.Column(db.Integer, db.ForeignKey('professional.id'), nullable=False)
    status = db.Column(SAEnum(StatusEnum), nullable=False, default=StatusEnum.PENDING)         #current status of the request --> pending, accepted, completed, cancelled
    assign_date = db.Column(db.DateTime, default=lambda: datetime.now(IST))
    accept_reject_date = db.Column(db.DateTime, nullable=True)
    completition_date = db.Column(db.DateTime, nullable=True)


class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    service_request_id = db.Column(db.Integer, db.ForeignKey('service_request.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False,default=0)
    payment_method = db.Column(db.String(120), nullable=False)   # payment method used by user --> Card, UPI, Wallet, Cash

    status = db.Column(SAEnum(StatusEnum), nullable=False, default=StatusEnum.PENDING)         #current status of the request --> pending, paid, failed
    payment_date = db.Column(db.DateTime, default=lambda: datetime.now(IST))
    bank_ref = db.Column(db.String(120), nullable=True)

    remarks = db.Column(db.String(120), nullable=True)

class ServiceReview(db.Model):
    __tablename__ = 'service_review'
    id = db.Column(db.Integer, primary_key=True)

    service_request_id = db.Column(db.Integer, db.ForeignKey('service_request.id'), nullable=False)
    rating = db.Column(db.Float, nullable=False)            # rating given by user to professional from 1 to 5
    review_text = db.Column(db.String(120), nullable=True)

    created_at = db.Column(db.DateTime, default=lambda: datetime.now(IST))
    updated_at = db.Column(db.DateTime, nullable=True)
    
class ProfessionalReview(db.Model):
    __tablename__ = 'professional_review'
    id = db.Column(db.Integer, primary_key=True)

    professional_id = db.Column(db.Integer, db.ForeignKey('professional.id'), nullable=False)
    rating = db.Column(db.Float, nullable=False)            # rating given by user to professional from 1 to 5
    review_text = db.Column(db.String(120), nullable=True)

    created_at = db.Column(db.DateTime, default=lambda: datetime.now(IST))
    updated_at = db.Column(db.DateTime, nullable=True)