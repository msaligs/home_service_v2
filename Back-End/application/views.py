
from flask import current_app as app, render_template, request, jsonify
from application.sec import datastore
from werkzeug.security import check_password_hash, generate_password_hash
from application.model import db, User, Professional
import random, string
from datetime import datetime

@app.get('/')
def home():
    return render_template('index.html')

@app.route('/user_login', methods=['POST'])
def user_login():
 
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({
            "success": False,
            "message": "Email and password are required.",
            "data": None
        }), 400

    user = datastore.find_user(email=email)

    if not user:
        return jsonify({
            "success": False,
            "message": "User not found.",
            "data": None
        }), 404

    if not user.active:
        return jsonify({
            "success": False,
            "message": "Your profile is not active yet. Please contact support.",
            "data": None
        }), 400

    if check_password_hash(user.password, password):
        return jsonify({
            "success": True,
            "message": "Login successful.",
            "data": {
                "token": user.get_auth_token(),
                "email": user.email,
                "role": user.roles[0].name
            }
        }), 200
    else:
        return jsonify({
            "success": False,
            "message": "Incorrect password.",
            "data": None
        }), 400

# @app.route('/register_user', methods=['POST'])
# def register_user():
#     try:
#         data = request.get_json()
#         name = data.get("name")
#         email = data.get("email")
#         password = data.get("password")
#         mobile = data.get("mobile")

#         # Basic validations
#         if not all([name, email, password, mobile]):
#             return jsonify({"error": "All fields are required"}), 400

#         if len(mobile) != 10 or not mobile.isdigit():
#             return jsonify({"error": "Mobile number must be exactly 10 digits"}), 400

#         # Check if user already exists
#         if datastore.find_user(email=email) or datastore.find_user(mobile=mobile):
#             return jsonify({"error": "Email or Mobile already registered"}), 409

#         # Create and store the user
#         user = datastore.create_user(
#             name=name,
#             email=email,
#             password=generate_password_hash(password),  # Hash password before saving
#             mobile=mobile,
#             roles=['user'],
#             active=True    
        
#         )
#         db.session.commit()  # Save to DB

#         return jsonify({"message": "User registered successfully"}), 201

#     except Exception as e:
#         return jsonify({"error": str(e)}), 500
    

# @app.route('/register-professional', methods=['POST'])
# def register_professional():
#     data = request.json
    
#     # Extract user data
#     name = data.get('name')
#     email = data.get('email')
#     password = data.get('password')
#     mobile = data.get('mobile')

#     # Extract professional data
#     category_id = data.get('category_id')
#     location_id = data.get('location_id')
#     experience = data.get('experience')
#     image_url = data.get('image_url', None)

#     # Check if email or mobile already exists
#     if datastore.find_user(email=email) or datastore.find_user(mobile=mobile):
#         return jsonify({"message": "Email or mobile already registered"}), 400

#     try:
#         # Create user
#         hashed_password = generate_password_hash(password)
#         new_user = datastore.create_user(
#             name=name,
#             email=email,
#             password=hashed_password,
#             mobile=mobile,
#         )
#         db.session.add(new_user)
#         db.session.flush()  # Get new user ID before committing

#         # Create professional profile
#         new_professional = Professional(
#             user_id=new_user.id,
#             category_id=category_id,
#             location_id=location_id,
#             experience=experience,
#             image_url=image_url
#         )
#         db.session.add(new_professional)

#         db.session.commit()  # Commit both records

#         # Send OTP email
#         # msg = Message('Verify Your Email', recipients=[email])
#         # msg.body = f'Your OTP code is {new_user.otp_code}. It expires in 10 minutes.'
#         # mail.send(msg)

#         return jsonify({"message": "Registration successful! Verify your email with OTP."}), 201
#     except Exception as e:
#         db.session.rollback()  # Rollback on error
#         return jsonify({"message": "Registration failed", "error": str(e)}), 500
