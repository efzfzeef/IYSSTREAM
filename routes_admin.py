from flask import Blueprint, jsonify, request
from models import User, db

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/api/admin/users', methods=['GET'])
def get_all_users():
    users = User.query.all()
    user_list = []
    for u in users:
        user_list.append({
            "id": u.id,
            "name": u.name,
            "email": u.email,
            "avatar": u.avatar or '',
            "role": u.role or 'member',
            "verified": bool(u.verified),
            "is_admin": bool(u.is_admin),
            "is_founder": bool(u.role == 'founder'),
            "created_at": u.created_at.strftime("%d/%m/%Y %H:%M")
        })
    return jsonify({"users": user_list})

@admin_bp.route('/api/admin/delete-user', methods=['POST'])
def delete_user():
    data = request.json
    email = data.get('email')
    current_email = data.get('current_email')
    
    if not email or not current_email:
        return jsonify({"erreur": "Email manquant."}), 400
    
    # Vérifier que l'utilisateur actuel est fondateur
    current_user = User.query.filter_by(email=current_email).first()
    if not current_user or current_user.role != 'founder':
        return jsonify({"erreur": "Seul le fondateur peut supprimer des utilisateurs."}), 403
    
    # Empêcher la suppression du fondateur lui-même
    if current_email == email:
        return jsonify({"erreur": "Vous ne pouvez pas vous supprimer vous-même."}), 403
    
    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({"erreur": "Utilisateur introuvable."}), 404
    
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "Utilisateur supprimé avec succès."}), 200

@admin_bp.route('/api/admin/role', methods=['POST'])
def update_role():
    data = request.json
    email = data.get('email')
    current_email = data.get('current_email')
    role = data.get('role')
    if not email or not current_email or role not in ['member', 'admin', 'founder']:
        return jsonify({"erreur": "Role invalide ou email manquant."}), 400
    if current_email == email:
        return jsonify({"erreur": "Vous ne pouvez pas modifier votre propre rôle."}), 403
    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({"erreur": "Utilisateur introuvable."}), 404
    user.role = role
    user.is_admin = True if role in ['admin', 'founder'] else False
    db.session.commit()
    return jsonify({"message": "Rôle mis à jour.", "user": {
        "name": user.name,
        "email": user.email,
        "role": user.role,
        "is_admin": user.is_admin,
        "verified": bool(user.verified),
        "created_at": user.created_at.strftime("%d/%m/%Y %H:%M")
    }}), 200