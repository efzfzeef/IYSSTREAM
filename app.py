import os
from flask import Flask, render_template
from models import db, User
from routes_admin import admin_bp
from routes_films import films_bp
from routes_anime import anime_bp
from routes_auth import auth_bp

app = Flask(__name__)

base_dir = os.path.abspath(os.path.dirname(__file__))
instance_dir = os.path.join(base_dir, 'instance')
os.makedirs(instance_dir, exist_ok=True)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(instance_dir, 'iysstream.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

app.register_blueprint(admin_bp)
app.register_blueprint(films_bp)
app.register_blueprint(anime_bp)
app.register_blueprint(auth_bp)

@app.route('/')
def home():
    return render_template('index.html')

def ensure_user_columns():
    with db.engine.connect() as conn:
        existing = [r[1] for r in conn.exec_driver_sql("PRAGMA table_info(user)").fetchall()]
        required = {
            'avatar': 'TEXT DEFAULT ""',
            'spotify': 'VARCHAR(255) DEFAULT ""',
            'youtube': 'VARCHAR(255) DEFAULT ""',
            'instagram': 'VARCHAR(255) DEFAULT ""',
            'twitch': 'VARCHAR(255) DEFAULT ""',
            'music_json': 'TEXT DEFAULT "[]"',
            'password_history': 'TEXT DEFAULT "[]"',
            'verified': 'BOOLEAN DEFAULT 0',
            'profile_color': 'VARCHAR(20) DEFAULT ""',
            'profile_style': 'VARCHAR(30) DEFAULT "default"',
            'profile_description': 'VARCHAR(255) DEFAULT ""',
            'profile_location': 'VARCHAR(100) DEFAULT ""',
            'profile_pronouns': 'VARCHAR(50) DEFAULT ""',
            'role': 'VARCHAR(30) DEFAULT "member"'
        }
        for name, col_type in required.items():
            if name not in existing:
                conn.exec_driver_sql(f'ALTER TABLE user ADD COLUMN {name} {col_type}')

with app.app_context():
    db.create_all()
    ensure_user_columns()

    admin_email = "kakashi.lopok@yahoo.com"
    admin_user = User.query.filter_by(email=admin_email).first()
    if not admin_user:
        admin_user = User(name="iys911", email=admin_email, is_admin=True, verified=True, role='founder')
        admin_user.set_password("Anamaghrebi212")
        db.session.add(admin_user)
        db.session.commit()
    elif admin_user.role != 'founder' or not admin_user.is_admin:
        admin_user.role = 'founder'
        admin_user.is_admin = True
        db.session.commit()

if __name__ == '__main__':
    app.run(debug=True, port=5000)
