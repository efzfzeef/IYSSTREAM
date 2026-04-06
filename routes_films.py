from flask import Blueprint, jsonify

films_bp = Blueprint('films', __name__)

@films_bp.route('/api/films/exclusivites', methods=['GET'])
def get_exclusive_films():
    return jsonify([])