from flask import Blueprint, jsonify

admin_bp = Blueprint('admin_bp', __name__)

@admin_bp.route('/dashboard', methods=['GET'])
def admin_dashboard():
    return jsonify({"message": "Admin Dashboard Access Granted"}), 200
