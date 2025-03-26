from flask import Blueprint, request, jsonify, current_app as app
from application.model import db, Professional, Category, Location, AssignRequest, ServiceRequest, IST, StatusEnum
from application.sec import datastore
from werkzeug.security import generate_password_hash
from flask_security import auth_required, roles_required, current_user
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError
from flask_security import auth_required, roles_required

professional_bp = Blueprint('professional_bp', __name__)

cache = app.cache

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
            profile_img_url = image_url,
            roles=['professional'],
            active=False
        )
        db.session.add(new_user)
        db.session.flush()  # Get new user ID before committing

        # Create professional profile
        new_professional = Professional(
            user_id=new_user.id,
            category_id=category_id,
            location_id=location_id,
            experience=experience,
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
@cache.cached(timeout=30)
def get_categories():
    # filter and fetch category data from database which is active
    categories = Category.query.filter_by(active=True).all()

    # return the data in json format
    return jsonify([{"id": c.id, "name": c.name} for c in categories])


@professional_bp.route('/get-locations', methods=['GET'])
@cache.cached(timeout=30)
def get_locations():
    # filter and fetch location data from database which is active
    locations = Location.query.filter_by(active=True).all()

    # return the data in json format
    return jsonify([{"id": l.id, "city": l.city, "state": l.state} for l in locations])


@professional_bp.route('/get-requests', methods=['GET'])
@auth_required('token')
@roles_required('professional')
@cache.memoize(timeout=30)
def get_request():
    try:
        # Get professional ID from current user
        professional_id = current_user.professional[0].id

        # Fetch requests with related data (efficient querying)
        requests = AssignRequest.query.filter_by(professional_id=professional_id).all()
        # service_name = ServiceRequest.query.get(r.service_request_id)

        # Prepare response data
        data = [{
           "id":r.id,
            "service_request_id":r.service_request_id,
            "service_name": ServiceRequest.query.get(r.service_request_id).service.name,
            "Service_description": ServiceRequest.query.get(r.service_request_id).service.description,
            "customer_address": ServiceRequest.query.get(r.service_request_id).user.user_address[0].address,
            "customer_city": ServiceRequest.query.get(r.service_request_id).user.user_address[0].location.city,
            "customer_state": ServiceRequest.query.get(r.service_request_id).user.user_address[0].location.state,
            "customer_pincode": ServiceRequest.query.get(r.service_request_id).user.user_address[0].pincode,
            "customer_mobile": ServiceRequest.query.get(r.service_request_id).user.mobile,
            "status": r.status.name,  # Ensure enum is converted to string
            "assign_date": r.assign_date.isoformat() if r.assign_date else None,
            "accept_reject_date": r.accept_reject_date.isoformat() if r.accept_reject_date else None,
            "completition_date": r.completition_date.isoformat() if r.completition_date else None
        } for r in requests]

        return jsonify(data), 200

    except Exception as e:
        return jsonify({"error": "Something went wrong", "details": str(e)}), 500
    

@professional_bp.route('/update-request-status/<int:request_id>', methods=['POST'])
@auth_required('token')
@roles_required('professional')
def update_request_status(request_id):
    try:
        data = request.get_json()
        status = data.get("status")

        # Validate the status input
        if status not in ["ACCEPTED", "REJECTED", "COMPLETED"]:
            return jsonify({"error": "Invalid status"}), 400

        # Find the request
        request_obj = AssignRequest.query.get(request_id)
        if not request_obj:
            return jsonify({"error": "Request not found"}), 404

        service_request = ServiceRequest.query.get(request_obj.service_request_id)
        if not service_request:
            return jsonify({"error": "Service request not found"}), 404
        
        # Prevent modifications to completed requests
        if request_obj.status.name == "COMPLETED":
            return jsonify({"error": "Completed requests cannot be modified"}), 400

        # Check if the logged-in professional owns this request
        professional_id = current_user.professional[0].id
        if request_obj.professional_id != professional_id:
            return jsonify({"error": "Unauthorized access"}), 403
        
        # Update status and timestamps
        now = datetime.now(IST)

        # Update status and timestamps
        if status == "ACCEPTED":
            request_obj.status = StatusEnum.ACCEPTED
            service_request.status = StatusEnum.ACCEPTED
            request_obj.accept_reject_date = now
        
        elif status == "REJECTED":
            request_obj.status = StatusEnum.REJECTED
            service_request.status = StatusEnum.REJECTED
            request_obj.accept_reject_date = now
        
        elif status == "COMPLETED":
            if request_obj.status != StatusEnum.ACCEPTED:
                return jsonify({"error": "Request must be accepted before completion"}), 400
            
            request_obj.status = StatusEnum.COMPLETED
            service_request.status = StatusEnum.COMPLETED
            service_request.completition_date = now
            request_obj.completition_date = now

        db.session.commit()
        return jsonify({"message": f"Request {status.lower()} successfully"}), 200

    except Exception as e:
        return jsonify({"error": "Something went wrong", "details": str(e)}), 500
    



@professional_bp.route('/profile', methods=['GET'])
@auth_required('token')
@roles_required('professional')
@cache.memoize(timeout=30)
def get_professional_profile():
    """Fetch professional profile details"""
    user_id = int(current_user.id)  # Get user ID from JWT token

    # Fetch professional details
    professional = Professional.query.filter_by(user_id=user_id).first()
    if not professional:
        return jsonify({'error': 'Professional profile not found'}), 404

    # Construct response data
    profile_data = {
        "id": professional.id,
        "name": professional.user.name,
        "email": professional.user.email,
        "mobile": professional.user.mobile,
        "profile_img_url": professional.user.profile_img_url,
        "category": professional.category.name if professional.category else None,
        "city": professional.location.city if professional.location else None,
        "state": professional.location.state if professional.location else None,
        "rating": professional.rating,
        "experience": professional.experience,
        "available": professional.available,
        "status": professional.status,
        "remarks": professional.remarks,
        "created_at": professional.created_at.strftime('%Y-%m-%d %H:%M:%S'),
        "updated_at": professional.updated_at.strftime('%Y-%m-%d %H:%M:%S') if professional.updated_at else None,
    }
    
    return jsonify(profile_data), 200



@professional_bp.route('/update-availability', methods=['PUT'])
@auth_required('token')
@roles_required('professional')
def update_availability():
    """Toggle professional availability status"""
    try:
        user_id = int(current_user.id)
        professional = Professional.query.filter_by(user_id=user_id).first()

        if not professional:
            return jsonify({'error': 'Professional profile not found'}), 404

        # Toggle availability
        professional.available = not professional.available
        db.session.commit()

        return jsonify({"message": "Availability status updated", "available": professional.available}), 200

    except ValueError:
        return jsonify({'error': 'Invalid user ID'}), 400
    except Exception as e:
        return jsonify({'error': 'An unexpected error occurred', 'details': str(e)}), 500





@professional_bp.route('/update-profile', methods=['PUT'])
@auth_required('token')
@roles_required('professional')
def update_profile():
    """Update the professional profile with enhanced error handling."""
    try:
        # Validate request JSON
        data = request.json
        if not data:
            return jsonify({'error': 'Invalid request, no data provided'}), 400

        # Extract parameters
        user_id = int(current_user.id)
        mobile = data.get('mobile')
        category_id = data.get('category_id')
        location_id = data.get('location_id')

        # Fetch professional profile
        professional = Professional.query.filter_by(user_id=user_id).first()
        if not professional:
            return jsonify({'error': 'Professional profile not found'}), 404

        # Track if any valid field was updated
        updated = False
        errors = []

        # Validate and update fields
        if mobile is not None:  # Check if key is present
            if not isinstance(mobile, str) or not mobile.isdigit() or len(mobile) != 10:
                errors.append('Invalid mobile number')
            else:
                professional.user.mobile = mobile
                updated = True

        if category_id is not None:
            category = Category.query.get(category_id)
            if not category:
                errors.append('Invalid category ID')
            else:
                professional.category_id = category_id
                updated = True

        if location_id is not None:
            location = Location.query.get(location_id)
            if not location:
                errors.append('Invalid location ID')
            else:
                professional.location_id = location_id
                updated = True

        # If no valid field was updated, return an error
        if not updated:
            return jsonify({'error': 'No valid fields provided', 'details': errors}), 400

        # Commit updates
        db.session.commit()
        return jsonify({"message": "Profile updated successfully"}), 200

    except SQLAlchemyError as e:
        db.session.rollback()  # Rollback in case of error
        return jsonify({'error': 'Database error occurred', 'details': str(e)}), 500

    except Exception as e:
        return jsonify({'error': 'An unexpected error occurred', 'details': str(e)}), 500
