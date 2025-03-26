
from flask import current_app as app, render_template, request, jsonify
from application.sec import datastore
from werkzeug.security import check_password_hash, generate_password_hash
from application.model import db, User, Professional
import random, string
from datetime import datetime


cache = app.cache
@app.get('/')
def home():
    return render_template('index.html')

@app.get('/cache')
@cache.cached(timeout=30)
def cache():
    return {"time": datetime.now()}

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
