from app import db, login_manager
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


# Flask-Login ko batata hai ki user kaise load karna hai
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# ─── TABLE 1: USER ───────────────────────────────────────
class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id            = db.Column(db.Integer, primary_key=True)
    name          = db.Column(db.String(100), nullable=False)
    email         = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    created_at    = db.Column(db.DateTime, default=datetime.utcnow)

    # ek user ke bahut saare symptom logs ho sakte hain
    symptom_logs  = db.relationship('SymptomLog', backref='user', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.email}>'


# ─── TABLE 2: CLINIC ─────────────────────────────────────
class Clinic(db.Model):
    __tablename__ = 'clinics'

    id         = db.Column(db.Integer, primary_key=True)
    name       = db.Column(db.String(150), nullable=False)
    address    = db.Column(db.String(300), nullable=False)
    city       = db.Column(db.String(100), nullable=False)
    district   = db.Column(db.String(100), nullable=False)
    state      = db.Column(db.String(100), nullable=False)
    phone      = db.Column(db.String(15))
    type       = db.Column(db.String(50))   # hospital / clinic / PHC
    latitude   = db.Column(db.Float)
    longitude  = db.Column(db.Float)
    added_by   = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Clinic {self.name}>'


# ─── TABLE 3: SYMPTOM LOG ────────────────────────────────
class SymptomLog(db.Model):
    __tablename__ = 'symptom_logs'

    id              = db.Column(db.Integer, primary_key=True)
    user_id         = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    symptoms_entered = db.Column(db.Text, nullable=False)
    ai_response     = db.Column(db.Text)
    timestamp       = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<SymptomLog {self.id}>'