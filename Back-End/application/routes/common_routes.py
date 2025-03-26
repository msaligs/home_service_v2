from flask import Blueprint, jsonify, request, current_app as app
from application.model import Location, ServiceLocation, Service
from sqlalchemy import and_

common_bp = Blueprint('common_bp', __name__)

cache = app.cache




@common_bp.route('/get-locations', methods=['GET'])
@cache.cached(timeout=30)
def get_location():
    state = request.args.get('state', None)

    # filter and fetch category data from database which is active
    query = Location.query.filter_by(active=True) #.order_by(Location.city).all()

    if state:
        query = query.filter(Location.state == state)
    
    locations = query.order_by(Location.city).all()

    # return the data in json format
    return jsonify([{"id": c.id, "city": c.city, "state":c.state } for c in locations])


@common_bp.route('/service-location/<int:location_id>', methods=['GET'])
# @cache.cached(timeout=30)
@cache.memoize(timeout=30)
def service_location(location_id):
    # filter and fetch category data from database which is active
    service_locations = ServiceLocation.query.filter(
            and_(ServiceLocation.active == True, ServiceLocation.location_id == location_id)
        ).all()

    # if service locations are not found return empty list
    if not service_locations:
        return jsonify([])
    
    return jsonify([
        {
            "id": sl.category.id if sl.category else None,
            "name": sl.category.name if sl.category else None,
        }
        for sl in service_locations
    ])


@common_bp.route('/services/<int:category_id>', methods=['GET'])
@cache.memoize(timeout=30)
def get_services_by_category(category_id):
    services = Service.query.filter_by(category_id=category_id, active=True).all()
    return jsonify([
        {
            "id": service.id,
            "name": service.name,
            "description": service.description,
            "image_url": service.image_url,
            "base_price": service.base_price
        }
        for service in services
    ])
