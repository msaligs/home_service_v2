from flask import Blueprint, jsonify, request
from application.model import User,Role, db, Professional, Category, Location, Service
from application.sec import datastore
from datetime import datetime
from pytz import timezone
from sqlalchemy import and_


# from application import db
IST = timezone('Asia/Kolkata')

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




@admin_bp.route('/user_detail/<int:id>', methods=['GET'])
def user_details(id):
    # Get the professional record for the user
    professional = Professional.query.filter_by(id=id).first()

    if not professional:
        return jsonify({"message": "Professional not found"}), 404

    # Prepare the response data
    professional_details = {
        'user_id': professional.user_id,
        'name': professional.user.name,
        'email': professional.user.email,
        'mobile': professional.user.mobile,
        'profile_img_url': professional.user.profile_img_url,
        'category': professional.category.name if professional.category else 'N/A',
        'location': professional.location.city if professional.location else 'N/A',
        'rating': professional.rating,
        'experience': professional.experience,
        'available': professional.available,
        'verified': professional.status,
        'created_at': professional.created_at.strftime('%Y-%m-%d %H:%M:%S'),
        'updated_at': professional.updated_at.strftime('%Y-%m-%d %H:%M:%S') if professional.updated_at else None   
    }
    return jsonify(professional_details), 200


@admin_bp.route('/get-categories', methods=['GET'])
def get_categories():
    # filter and fetch category data from database which is active
    categories = Category.query.filter_by(active=True).order_by(Category.name).all()

    # return the data in json format
    return jsonify([{"id": c.id, "name": c.name, "description":c.description } for c in categories])





@admin_bp.route('/add-location', methods=['POST'])
def add_location():
    data = request.json
    city = data.get('city')
    state = data.get('state')

    if not city or not state:
        return jsonify({"message": "City and state are required"}), 400

    location = Location(city=city, state=state)
    db.session.add(location)
    db.session.commit()

    return jsonify({"message": "Location added successfully"}), 201

@admin_bp.route('/add-category', methods=['POST'])
def add_category():
    data = request.json
    name = data.get('name')
    description = data.get('description')
    image_url = data.get('image_url')

    if not name:
        return jsonify({"message": "Category name is required"}), 400

    category = Category(name=name, description=description, image_url=image_url)
    db.session.add(category)
    db.session.commit()

    return jsonify({"message": "Category added successfully"}), 201

@admin_bp.route('/update-category/<int:id>', methods=['PUT'])
def update_category(id):
    data = request.json
    name = data.get('name')
    description = data.get('description')
    image_url = data.get('image_url')

    category = Category.query.get(id)
    if not category:
        return jsonify({"message": "Category not found"}), 404

    category.name = name
    category.description = description
    category.image_url = image_url

    db.session.commit()
    return jsonify({"message": "Category updated successfully"}), 200

@admin_bp.route('/update-location/<int:id>', methods=['PUT'])
def update_location(id):
    data = request.json
    city = data.get('city')
    state = data.get('state')

    location = Location.query.get(id)
    if not location:
        return jsonify({"message": "Location not found"}), 404
    
    location.city = city
    location.state = state

    db.session.commit()
    return jsonify({"message": "Location updated successfully"}), 200



@admin_bp.route('/get-locations', methods=['GET'])
def get_locations():
    # filter and fetch location data from database which is active
    locations = Location.query.filter_by(active=True).order_by(Location.state).all()

    # return the data in json format
    return jsonify([{"id": l.id, "city": l.city, "state": l.state} for l in locations])
 

@admin_bp.route('/professionals', methods=['GET'])
def get_professionals():
    filter_status = request.args.get('filter', 'all')  # Get filter from query params
    search_query = request.args.get('search', '').strip().lower()  # Get search input
    category_filter = request.args.get('category', '').strip()
    location_filter = request.args.get('location', '').strip()

    # Define base query with necessary joins
    query = Professional.query.join(User)

    # Apply status filter
    if filter_status in ['pending', 'verified', 'rejected']:
        if filter_status == 'pending':
            query = query.filter(and_(Professional.status == filter_status, User.active == True))
        else:
            query = query.filter(Professional.status == filter_status)


    # Apply search query (by name or email)
    if search_query:
        query = query.filter(
            (User.name.ilike(f"%{search_query}%")) | (User.email.ilike(f"%{search_query}%"))
        )

    # Filter by category ID if provided
    if category_filter:
        query = query.filter(Professional.category_id == category_filter)

    # Filter by location ID if provided
    if location_filter:
        query = query.filter(Professional.location_id == location_filter)

    professionals = query.all()

    results = [{
        "id": p.id,
        "name": p.user.name,  # Access User's name via relationship
        "email": p.user.email,  # Access User's email
        "mobile": p.user.mobile,  # Access User's mobile
        "experience": p.experience,
        "active": p.user.active,
        "status": p.status,
        "category": p.category.name,  # Fetch category name via relationship
        "location": p.location.city  # Fetch location via relationship
    } for p in professionals]

        # user_id': user_id,

        # 'name': professional.user.name,
        # 'email': professional.user.email,
        # 'mobile': professional.user.mobile,
        # 'experience': professional.experience,
        # 'category': professional.category.name if professional.category else 'N/A',
        # 'location': professional.location.city if professional.location else 'N/A',

        # 'profile_img_url': professional.user.profile_img_url,
        # 'rating': professional.rating,
        # 'available': professional.available,
        # 'verified': professional.status,
        # 'created_at': professional.created_at.strftime('%Y-%m-%d %H:%M:%S'),
        # 'up

    return jsonify(results)



@admin_bp.route('/update_professional_status/<int:professional_id>', methods=['POST'])
def update_professional_status(professional_id):
    data = request.json  # Expecting {"status": "verified"} or {"status": "rejected"} 

    professional = Professional.query.get(professional_id)
    if not professional:
        return jsonify({"message": "Professional not found"}), 404

    # Fetch associated user
    user = User.query.get(professional.user_id)  # Assuming Professional has user_id FK
    if not user or not user.active:
        return jsonify({"message": "User must verify email and mobile before being approved"}), 400

    if data.get("status") not in ["verified", "rejected"]:
        return jsonify({"message": "Invalid status"}), 400

    # Prevent re-verification or re-rejection
    if professional.status == data.get("status"):
        return jsonify({"message": f"Professional is already {data.get('status')}"}), 400

    # Update status and timestamp
    professional.status = data.get("status")
    professional.status_updated_at = datetime.now(IST)

    try:
        db.session.commit()
        return jsonify({
            "message": f"Professional {data.get('status')} successfully",
            "updated_at": professional.status_updated_at
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Something went wrong", "error": str(e)}), 500



@admin_bp.route('/get-services', methods=['GET'])
def get_services():
    services = Service.query.join(Category).filter(Service.active == True).all()
    return jsonify([
        {
            "id": s.id,
            "name": s.name,
            "description": s.description,
            "image_url": s.image_url,
            "base_price": s.base_price,
            "category_name": s.category.name,  # Include category name
            "active": s.active
        }
        for s in services
    ])

@admin_bp.route('/add-service', methods=['POST'])
def add_service():
    data = request.json
    name = data.get('name')
    description = data.get('description')
    image_url = data.get('image_url')
    base_price = data.get('base_price')
    category_id = data.get('category_id')

    if not name or not category_id:
        return jsonify({"message": "Name and category ID are required"}), 400

    service = Service(name=name, description=description, image_url=image_url, base_price=base_price, category_id=category_id)
    db.session.add(service)
    db.session.commit()

    return jsonify({"message": "Service added successfully"}), 201

# to delete a service
@admin_bp.route('/delete-service/<int:id>', methods=['DELETE'])
def delete_service(id):
    service = Service.query.get(id)
    if not service:
        return jsonify({"message": "Service not found"}), 404

    db.session.delete(service)
    db.session.commit()

    return jsonify({"message": "Service deleted successfully"}), 200


@admin_bp.route('/update-service/<int:id>', methods=['PUT'])
def update_service(id):
    data = request.json
    name = data.get('name')
    description = data.get('description')
    image_url = data.get('image_url')
    base_price = data.get('base_price')
    category_id = data.get('category_id')

    service = Service.query.get(id)
    if not service:
        return jsonify({"message": "Service not found"}), 404

    service.name = name
    service.description = description
    service.image_url = image_url
    service.base_price = base_price
    service.category_id = category

    db.session.commit()

    return jsonify({"message": "Service updated successfully"}), 200

# @admin_bp.route('/toggle-service/<int:service_id>', methods=['GET'])
# def toggle_service_activation(service_id):
#     service = Service.query.get(service_id)
#     if not service:
#         return jsonify({"message": "Service not found"}), 404

#     # Toggle service activation status
#     service.active = not service.active
#     db.session.commit()

#     return jsonify({"message": f"Service {'activated' if service.active else 'deactivated'} successfully"}), 200


