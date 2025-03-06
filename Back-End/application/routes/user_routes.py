from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash
from flask_security import auth_required, current_user, roles_required
from application.model import db, User, ServiceRequest, StatusEnum
from application.sec import datastore
from sqlalchemy.exc import IntegrityError
from sqlalchemy import desc

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
    

@user_bp.route('/book_service/<int:service_id>', methods=['POST'])
@auth_required('token')
def book_service(service_id):
    try:
        # Get JSON payload
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid or missing JSON payload"}), 400

        # Extract and validate required fields
        user_id = int(current_user.id)  # Ensure it gets an integer ID
        price = data.get("price", None)  # Explicit default value
        remarks = data.get("remarks", "")  # Default to empty string

        if price is None:
            return jsonify({"error": "Price is required"}), 400

        # Check if the user already has a pending or accepted request for the service
        existing_request = ServiceRequest.query.filter(
            ServiceRequest.user_id == user_id,
            ServiceRequest.service_id == service_id,
            ServiceRequest.status.in_([StatusEnum.PENDING, StatusEnum.ACCEPTED])  # Use Enum values
        ).first()

        if existing_request:
            return jsonify({
                "error": "You already have an active request for this service.",
                "existing_request": {
                    "id": existing_request.id,
                    "status": existing_request.status.name,  # Convert Enum to string
                    "requested_at": existing_request.request_date
                }
            }), 409


        # Create and store the booking
        booking = ServiceRequest(
            user_id=user_id,
            service_id=service_id,
            total_price=price,
            remarks=remarks,
            status=StatusEnum.PENDING
        )
        
        db.session.add(booking)
        db.session.commit()  # Commit the transaction
        # import time
        # time.sleep(10)
        return jsonify({
            "message": "Booking successful",
            "data": {
            "user_id": user_id,
            "service_id": service_id,
            "price": price,
            "remarks": remarks
            }
        }), 201

    except IntegrityError:
        db.session.rollback()  # Rollback in case of DB errors
        return jsonify({"error": "Database integrity error. Please try again."}), 500

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "An unexpected error occurred", "details": str(e)}), 500


@user_bp.route('/get_bookings', methods=['GET'])
@auth_required('token')
@roles_required('user')
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
