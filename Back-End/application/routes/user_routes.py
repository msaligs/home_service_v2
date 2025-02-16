from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash
from application.model import db, User
from application.sec import datastore

user_bp = Blueprint('user_bp', __name__)


@user_bp.route('/register_user', methods=['POST'])
def register_user():
    try:
        data = request.get_json()
        name = data.get("name")
        email = data.get("email")
        password = data.get("password")
        mobile = data.get("mobile")

        # Basic validations
        if not all([name, email, password, mobile]):
            return jsonify({"error": "All fields are required"}), 400

        if len(mobile) != 10 or not mobile.isdigit():
            return jsonify({"error": "Mobile number must be exactly 10 digits"}), 400

        # Check if user already exists
        if datastore.find_user(email=email) or datastore.find_user(mobile=mobile):
            return jsonify({"error": "Email or Mobile already registered"}), 409

        # Create and store the user
        user = datastore.create_user(
            name=name,
            email=email,
            password=generate_password_hash(password),  # Hash password before saving
            mobile=mobile,
            roles=['user'],
            active=True    
        
        )
        db.session.commit()  # Save to DB

        return jsonify({"message": "User registered successfully"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
