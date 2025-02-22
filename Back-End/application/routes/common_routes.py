from flask import Blueprint, jsonify, request
from application.model import Location, ServiceLocation, Service
from sqlalchemy import and_

common_bp = Blueprint('common_bp', __name__)






@common_bp.route('/get-locations', methods=['GET'])
def get_location():
    # filter and fetch category data from database which is active
    locations = Location.query.filter_by(active=True).order_by(Location.city).all()

    # return the data in json format
    return jsonify([{"id": c.id, "city": c.city, "state":c.state } for c in locations])


@common_bp.route('/service-location/<int:location_id>', methods=['GET'])
def service_location(location_id):
    # filter and fetch category data from database which is active
    service_locations = ServiceLocation.query.filter(
            and_(ServiceLocation.active == True, ServiceLocation.location_id == location_id)
        ).all()

    # return the data in json format
    # return jsonify([{"id": c.id, "name": c.name} for c in categories])
    # return service_location
    return jsonify([
        {
            "id": sl.category.id,
            "name": sl.category.name
        }
        for sl in service_locations
    ])


@common_bp.route('/services/<int:category_id>', methods=['GET'])
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
