from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash
from models import db, User
import smtplib
from email.mime.text import MIMEText
import random

auth_bp = Blueprint('auth', __name__)

# On garde les codes temporairement en mémoire
utilisateurs_en_attente = {}

def envoyer_mail_code(email_destinataire, code):
    email_expediteur = "bendahouilyas09@gmail.com"
    mot_de_passe_app = "sduahgzddgixxbti" 

    msg = MIMEText(f"Bienvenue sur iysSTREAM ! \n\nVotre code de vérification est : {code}\n\nNe le partagez avec personne.")
    msg['Subject'] = 'Code de vérification iysSTREAM'
    msg['From'] = email_expediteur
    msg['To'] = email_destinataire

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(email_expediteur, mot_de_passe_app)
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        print("Erreur d'envoi de mail :", e)
        return False

# --- 1. DEMANDE D'INSCRIPTION ---
@auth_bp.route('/api/auth/register', methods=['POST'])
def register():
    data = request.json
    email = data.get('email')
    
    # Vérifier si l'email existe déjà dans la vraie Base de Données
    if User.query.filter_by(email=email).first():
        return jsonify({"erreur": "Cet email est déjà utilisé."}), 400

    # Générer le code
    code_secret = str(random.randint(100000, 999999))
    
    # Sauvegarder les infos en attendant le code
    utilisateurs_en_attente[email] = {
        "name": data.get('name'),
        "password": data.get('password'),
        "code": code_secret
    }

    if envoyer_mail_code(email, code_secret):
        return jsonify({"message": "Code envoyé"}), 200
    else:
        return jsonify({"erreur": "Erreur d'envoi du mail."}), 500

# --- 2. VÉRIFICATION DU CODE ---
@auth_bp.route('/api/auth/verify', methods=['POST'])
def verify():
    data = request.json
    email = data.get('email')
    code = data.get('code')

    user_temp = utilisateurs_en_attente.get(email)
    if not user_temp:
        return jsonify({"erreur": "Session expirée ou email invalide."}), 400

    if user_temp['code'] == code:
        # Code bon ! On crée le compte dans la vraie DB
        nouvel_utilisateur = User(name=user_temp['name'], email=email)
        nouvel_utilisateur.set_password(user_temp['password'])
        db.session.add(nouvel_utilisateur)
        db.session.commit()
        del utilisateurs_en_attente[email]
        
        # On renvoie les infos pour connecter le gars direct
        return jsonify({
            "message": "Compte créé", 
            "user": {"name": nouvel_utilisateur.name, "email": nouvel_utilisateur.email, "isAdmin": nouvel_utilisateur.is_admin}
        }), 200
    else:
        return jsonify({"erreur": "Code incorrect."}), 400

# --- 3. CONNEXION (LOGIN) ---
@auth_bp.route('/api/auth/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(email=data.get('email')).first()
    if user and user.check_password(data.get('password')):
        return jsonify({
            "message": "Connecté",
            "user": {"name": user.name, "email": user.email, "isAdmin": user.is_admin}
        }), 200
    return jsonify({"erreur": "Email ou mot de passe incorrect."}), 400