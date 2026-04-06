from flask import Blueprint, jsonify

anime_bp = Blueprint('anime', __name__)

@anime_bp.route('/api/anime/exclusivites', methods=['GET'])
def get_exclusive_anime():
    return jsonify([])