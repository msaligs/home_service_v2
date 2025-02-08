from flask import current_app as app, render_template, redirect, url_for, request, jsonify
from flask_security import auth_required, current_user
from application.model import *
from application.sec import datastore
from werkzeug.security import check_password_hash


@app.get('/')
def home():
    return render_template('index.html')

@app.route('/user_login', methods=['GET', 'POST'])
def user_login():
    if request.method == 'GET':
        return render_template('login.html')
    
    elif request.method == 'POST':
        data = request.get_json()
        email = data.get('email')
        if not email:
            return jsonify({"message": "Email not provided"}), 400

        user = datastore.find_user(email=email)


        if not user:
            return jsonify({"message": "User Not Found"}), 404
        if not user.active:
            return jsonify({"message": "Your profile is not active yet."}), 400

        if user.active and  check_password_hash(user.password, data.get("password")):
            return jsonify({"token": user.get_auth_token(), "email": user.email, "role": user.roles[0].name})
        else:
            return jsonify({"message": "Wrong Password"}), 400