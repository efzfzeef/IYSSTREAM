from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    avatar = db.Column(db.Text, default='')
    spotify = db.Column(db.String(255), default='')
    youtube = db.Column(db.String(255), default='')
    instagram = db.Column(db.String(255), default='')
    twitch = db.Column(db.String(255), default='')
    music_json = db.Column(db.Text, default='[]')
    verified = db.Column(db.Boolean, default=False)
    profile_color = db.Column(db.String(20), default='')
    profile_style = db.Column(db.String(30), default='default')
    profile_description = db.Column(db.String(255), default='')
    profile_location = db.Column(db.String(100), default='')
    profile_pronouns = db.Column(db.String(50), default='')
    role = db.Column(db.String(30), default='member')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)