from flask import Blueprint, jsonify, request
from application.model import Category

professional_bp = Blueprint('professional_bp', __name__)




@professional_bp.route('/get-categories', methods=['GET'])
def get_categories():
    # filter and fetch category data from database which is active
    categories = Category.query.filter_by(active=True).all()

    # return the data in json format
    return jsonify([{"id": c.id, "name": c.name} for c in categories])
