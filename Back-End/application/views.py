
from flask import current_app as app, render_template, request, jsonify
from application.sec import datastore
from werkzeug.security import check_password_hash, generate_password_hash
from application.model import db

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

@app.route('/register_user', methods=['POST'])
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