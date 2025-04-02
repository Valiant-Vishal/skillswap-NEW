from datetime import datetime
from extensions import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

# User Table
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    name = db.Column(db.String(100))
    location = db.Column(db.String(100))
    bio = db.Column(db.Text)
    profile_pic = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    skills = db.relationship('Skill', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    sent_messages = db.relationship('Message', foreign_keys='Message.sender_id', backref='sender', lazy='dynamic')
    received_messages = db.relationship('Message', foreign_keys='Message.receiver_id', backref='receiver', lazy='dynamic')
    # Connection requests are defined via backrefs in the ConnectionRequest model

    def set_password(self, password):
        """Hash the password and store it in the password_hash attribute."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Check the provided password against the stored password hash."""
        return check_password_hash(self.password_hash, password)
    
    def get_known_skills(self):
        """Return skills that the user knows."""
        return [skill.name.lower() for skill in self.skills.filter_by(category='known').all()]
    
    def get_learning_skills(self):
        """Return skills that the user wants to learn."""
        return [skill.name.lower() for skill in self.skills.filter_by(category='learning').all()]
    
    def has_connection_with(self, user_id):
        """Check if there's an existing connection request between users."""
        from_me = ConnectionRequest.query.filter_by(sender_id=self.id, receiver_id=user_id).first()
        to_me = ConnectionRequest.query.filter_by(sender_id=user_id, receiver_id=self.id).first()
        return from_me or to_me

# Skill Table
class Skill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)  # known, learning, recommended
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # Foreign Key
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Message Table
class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Foreign Key
    receiver_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Foreign Key
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Connection Request Table
class ConnectionRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Foreign Key
    receiver_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Foreign Key
    status = db.Column(db.String(20), default='pending')  # pending, accepted, rejected
    matched_skill_id = db.Column(db.Integer, db.ForeignKey('skill.id'))
    requested_skill_id = db.Column(db.Integer, db.ForeignKey('skill.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    sender = db.relationship('User', foreign_keys=[sender_id], backref='sent_requests')
    receiver = db.relationship('User', foreign_keys=[receiver_id], backref='received_requests')
    matched_skill = db.relationship('Skill', foreign_keys=[matched_skill_id])
    requested_skill = db.relationship('Skill', foreign_keys=[requested_skill_id])
