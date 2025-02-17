from flask import Blueprint, jsonify, request
from application.model import User,Role, db, Professional, Category, Location
from application.sec import datastore
# from application import db


admin_bp = Blueprint('admin_bp', __name__)

@admin_bp.route('/dashboard', methods=['GET'])
def admin_dashboard():
    return jsonify({"message": "Admin Dashboard Access Granted"}), 200


@admin_bp.route('/users', methods=['GET'])
def users():
    # Get page number and items per page from request args (default: page 1, 10 items per page)
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    role = request.args.get('role', '', type=str)
    status = request.args.get('status', '', type=str)

    # Build the base query
    query = User.query.filter(User.id != 1)  # Exclude admin with id=1

    # Apply role filter if provided
    if role:
        # query = query.join(User.roles).filter(Role.name == role)
        query = query.join(User.roles).filter(Role.name.ilike(role))


    # Apply status filter if provided
    if status:
        is_active = True if status == 'true' else False
        query = query.filter(User.active == is_active)

    # Paginate the query
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)

    # Extract user data
    users = [{
        "id": u.id,
        "name": u.name,
        "email": u.email,
        "mobile": u.mobile,
        "active": u.active,
        "role": u.roles[0].name if u.roles else None,
        "created_at": u.created_at,
        "updated_at": u.updated_at
    } for u in pagination.items]

    return jsonify({
        'users': users,
        'total_pages': pagination.pages,
        'current_page': pagination.page
    })



@admin_bp.route('/toggle_user/<int:user_id>', methods=['GET'])
def toggle_user_activation(user_id):
    user = datastore.find_user(id=user_id)
    
    if user:
        # Check if the user is already active
        if user.active:
            # Deactivate the user
            user.active = False
            db.session.commit()
            return jsonify({"message": "User deactivated successfully"}), 200
        else:
            # Activate the user
            user.active = True
            db.session.commit()
            return jsonify({"message": "User activated successfully"}), 200

    return jsonify({"message": "User not found"}), 404




@admin_bp.route('/user_details/<int:user_id>', methods=['GET'])
def user_details(user_id):
    # Get the professional record for the user
    professional = Professional.query.filter_by(user_id=user_id).first()

    if not professional:
        return jsonify({"message": "Professional not found"}), 404

    # Get related user information
    user = User.query.get(user_id)
    category = Category.query.get(professional.category_id)
    location = Location.query.get(professional.location_id)

    # Prepare the response data
    professional_details = {
        'user_id': user.id,
        'name': user.name,
        'email': user.email,
        'mobile': user.mobile,
        'profile_img_url': user.profile_img_url,
        'category': category.name if category else 'N/A',
        'location': location.city if location else 'N/A',
        'rating': professional.rating,
        'experience': professional.experience,
        'available': professional.available,
        'verified': professional.verified,
        'created_at': professional.created_at.strftime('%Y-%m-%d %H:%M:%S'),
        'updated_at': professional.updated_at.strftime('%Y-%m-%d %H:%M:%S') if professional.updated_at else None,
        'image_url': professional.image_url
    }

    return jsonify(professional_details), 200
