from flask import Blueprint, request, jsonify
from application.model import db, Professional, Category, Location, User
from application.sec import datastore
from werkzeug.security import generate_password_hash

professional_bp = Blueprint('professional_bp', __name__)

@professional_bp.route('/register-professional', methods=['POST'])
def register_professional():
    data = request.json
    
    # Extract user data
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    mobile = data.get('mobile')

    # Extract professional data
    category_id = data.get('category_id')
    location_id = data.get('location_id')
    experience = data.get('experience')
    image_url = data.get('image_url', None)

    # Check if email or mobile already exists
    if datastore.find_user(email=email) or datastore.find_user(mobile=mobile):
        return jsonify({"message": "Email or mobile already registered"}), 400

    try:
        # Create user
        hashed_password = generate_password_hash(password)
        new_user = datastore.create_user(
            name=name,
            email=email,
            password=hashed_password,
            mobile=mobile,
        )
        db.session.add(new_user)
        db.session.flush()  # Get new user ID before committing

        # Create professional profile
        new_professional = Professional(
            user_id=new_user.id,
            category_id=category_id,
            location_id=location_id,
            experience=experience,
            image_url=image_url
        )
        db.session.add(new_professional)

        db.session.commit()  # Commit both records

        # Send OTP email
        # msg = Message('Verify Your Email', recipients=[email])
        # msg.body = f'Your OTP code is {new_user.otp_code}. It expires in 10 minutes.'
        # mail.send(msg)

        return jsonify({"message": "Registration successful! Verify your email with OTP."}), 201
    except Exception as e:
        db.session.rollback()  # Rollback on error
        return jsonify({"message": "Registration failed", "error": str(e)}), 500



@professional_bp.route('/get-categories', methods=['GET'])
def get_categories():
    # filter and fetch category data from database which is active
    categories = Category.query.filter_by(active=True).all()

    # return the data in json format
    return jsonify([{"id": c.id, "name": c.name} for c in categories])


@professional_bp.route('/get-locations', methods=['GET'])
def get_locations():
    # filter and fetch location data from database which is active
    locations = Location.query.filter_by(active=True).all()

    # return the data in json format
    return jsonify([{"id": l.id, "city": l.city, "state": l.state} for l in locations])
