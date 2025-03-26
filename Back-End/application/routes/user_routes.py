from flask import Blueprint, request, jsonify,current_app as app
from werkzeug.security import generate_password_hash
from flask_security import auth_required, current_user, roles_required
from application.model import db, User, ServiceRequest, StatusEnum, Professional, Service, UserAddress, ServiceLocation, AssignRequest
from application.sec import datastore
from sqlalchemy.exc import IntegrityError
from sqlalchemy import desc, and_
from werkzeug.exceptions import BadRequest

user_bp = Blueprint('user_bp', __name__)

cache = app.cache

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


@user_bp.route('/user_address', methods=['GET'])  
@auth_required('token')
@roles_required('user')
@cache.memoize(timeout=30)
def get_user_address():
    user = current_user
    user_address = user.user_address[0] if user.user_address else None
    print(user_address)
    if user_address:
        return jsonify({
            "message": "User address found",
            "data": {
                "address": user_address.address,
                "city": user_address.location.city,
                "state": user_address.location.state,
                "pincode": user_address.pincode
            }
        }), 200
    return jsonify({"message": "User address not found"}), 404 

@user_bp.route('/add_address', methods=['POST'])
@auth_required('token')
@roles_required('user')
def add_address():
    try:
        data = request.get_json()
        user = current_user
        address = data.get("address")
        location_id = data.get("location_id")
        pincode = data.get("pincode")

        if not all([address, location_id, pincode]):
            return jsonify({"error": "All fields are required"}), 400

        # Create a new UserAddress entry
        new_address = UserAddress(
            user_id=user.id,
            address=address,
            location_id=location_id,
            pincode=pincode
        )

        db.session.add(new_address)  # Add to session
        db.session.commit()  # Commit changes

        return jsonify({"message": "Address added successfully"}), 201

    except Exception as e:
        db.session.rollback()  # Rollback in case of error
        return jsonify({"error": str(e)}), 500



@user_bp.route('/update_address', methods=['PUT'])
@auth_required('token')
@roles_required('user')
def update_address():
    try:
        data = request.get_json()
        user = current_user
        address = data.get("address")
        location_id = data.get("location_id")
        pincode = data.get("pincode")

        if not all([address, location_id, pincode]):
            return jsonify({"error": "All fields are required"}), 400

        # Fetch the existing address
        user_address = user.user_address[0] if user.user_address else None
        if not user_address:
            return jsonify({"error": "User address not found"}), 404

        # Update the address fields
        user_address.address = address
        user_address.location_id = location_id
        user_address.pincode = pincode

        db.session.commit()  # Commit changes

        return jsonify({"message": "Address updated successfully"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
    
    

@user_bp.route('/book_service/<int:service_id>', methods=['POST'])
@auth_required('token')
@roles_required('user')
def book_service(service_id):
    try:
        # Check if the service exists
        service = Service.query.get(service_id)
        if not service:
            return jsonify({
                "message": "Requested service not found.",
                "status": "error"
            }), 404
        

        # Extract and validate JSON payload
        data = request.get_json()
        if not data:
            return jsonify({
                "message": "Requested details missing.",
                "status": "error"
            }), 400

        # Extract and validate required fields
        user_id = int(current_user.id)  
        user_location = current_user.user_address[0] if current_user.user_address else None  

        if not user_location:
            return jsonify({
                "message": "Please add your address before booking a service.",
                "status": "error"
            }), 400

        # Validate if service is available in user's location
        user_location_id = user_location.location_id
        selected_service_category_id = service.category_id

        service_location = ServiceLocation.query.filter(
            and_(ServiceLocation.location_id == user_location_id, 
                 ServiceLocation.category_id == selected_service_category_id)
        ).first()

        if not service_location:
            return jsonify({
                "message": "This Category services are not available at your location. Please update your city.",
                "status": "error"
            }), 400

        # Validate price
        price = data.get("price")
        if price is None:
            return jsonify({
                "message": "Price is required.",
                "status": "error"
            }), 400

        category_id = service.category.id
        remarks = data.get("remarks", "")  

        # Check if user already has an active request
        existing_request = ServiceRequest.query.filter(
            ServiceRequest.user_id == user_id,
            ServiceRequest.service_id == service_id,
            ServiceRequest.status.in_([StatusEnum.PENDING, StatusEnum.ACCEPTED, StatusEnum.ASSIGNED])
        ).first()

        if existing_request:
            return jsonify({
                "message": "You already have an active request for this service.",
                "status": "error"
            }), 409

        # Find an available professional
        professional = Professional.query.filter(
            Professional.user.has(active=True),
            Professional.available == True,
            # Professional.category_id == category_id,  
            Professional.location_id == user_location_id
        ).first()

        # Create and save the booking request
        booking = ServiceRequest(
            user_id=user_id,
            service_id=service_id,
            location_id=user_location_id,
            professional_id=professional.id if professional else None,
            total_price=price,
            remarks=remarks,
            status=StatusEnum.ASSIGNED if professional else StatusEnum.PENDING
        )
        db.session.add(booking)
        db.session.flush()

        if professional:
            assign = AssignRequest(service_request_id=booking.id, professional_id=professional.id, status = StatusEnum.ASSIGNED)
            db.session.add(assign)

        db.session.commit()

        return jsonify({
            "message": "Booking successful.",
            "status": "success",
            "data": {
                "user_id": user_id,
                "service_id": service_id,
                "service_name": service.name,
                "Professional": professional.user.name if professional else "Not assigned",
                "price": price,
                "remarks": remarks
            }
        }), 201
    
    

    except IntegrityError as e:
        db.session.rollback()
        return jsonify({
            "message": "Database integrity error. Please try again.",
            "status": "error",
            "details": str(e)
        }), 500

    except BadRequest as e:
        return jsonify({
            "message": "Invalid request data.",
            "status": "error",
            "details": str(e)
        }), 400

    except Exception as e:
        db.session.rollback()
        return jsonify({
            "message": "An unexpected error occurred.",
            "status": "error",
            "details": str(e)
        }), 500


@user_bp.route('/get_bookings', methods=['GET'])
@auth_required('token')
@roles_required('user')
@cache.memoize(timeout=30)
def get_bookings():
    user_id = current_user.id
    bookings = ServiceRequest.query.filter(ServiceRequest.user_id == user_id).order_by(desc(ServiceRequest.request_date)).all()
    # return bookings # This is for testing purposes only
    response = []
    for booking in bookings:
        response.append({
            "id": booking.id,
            "service_id": booking.service_id,
            "service_name": booking.service.name,
            "total_price": booking.total_price,
            "remarks": booking.remarks,
            "status": booking.status.name,  # Convert Enum to string
            "professional": booking.professional.user.name if booking.professional else "",
            "completition_date": booking.completition_date.isoformat() if booking.completition_date else None,
            "requested_at": booking.request_date
        })
    return jsonify({"message":"Successfully fetched",
                    "data":response}), 200



# endpoint to cancel a booking
@user_bp.route('/cancel_request/<int:booking_id>', methods=['DELETE'])
@auth_required('token')
@roles_required('user')
def cancel_booking(booking_id):
    try:
        user_id = current_user.id
        booking = ServiceRequest.query.filter(ServiceRequest.user_id == user_id, 
                                              ServiceRequest.id == booking_id).first()

        # Check if booking exists
        if not booking:
            return jsonify({"error": "Booking not found"}), 404

        # Check if the booking is already processed and cannot be canceled
        if booking.status not in [StatusEnum.PENDING]:
            return jsonify({"error": "This booking cannot be canceled at its current status."}), 400

        # Ensure the service exists before accessing its attributes
        if not booking.service:
            return jsonify({"error": "Service details not found"}), 500

        # Cancel the booking
        booking.status = StatusEnum.CANCELLED
        db.session.commit()

        return jsonify({
            "message": "Booking canceled successfully",
            "data": {
                "service_id": booking.id,
                "name": booking.service.name,
                "price": booking.total_price,
                "request_date": booking.request_date,
                "status": booking.status.name,
                "remarks": booking.remarks or "No remarks"
            }
        }), 200

    except Exception as e:
        db.session.rollback()  # Rollback in case of an error
        return jsonify({"error": "An error occurred while canceling the booking.", "details": str(e)}), 500



@user_bp.route('/profile', methods=['GET'])
@auth_required('token')
@roles_required('user')
@cache.memoize(timeout=30)
def get_profile():
    """Fetch user profile details"""
    user_id = int(current_user.id)  # Get user ID from JWT token

    # Fetch professional details
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'user profile not found'}), 404

    # Construct response data
    profile_data = {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "mobile": user.mobile,
        "profile_img_url": user.profile_img_url,
   
        "created_at": user.created_at.strftime('%Y-%m-%d %H:%M:%S'),
        "updated_at": user.updated_at.strftime('%Y-%m-%d %H:%M:%S') if user.updated_at else None,
    }
    
    return jsonify(profile_data), 200
