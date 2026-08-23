import re
from app import bcrypt, db
from app.models.basemodel import BaseModel

user_favorites = db.Table('user_favorites',
    db.Column('user_id', db.String(36), db.ForeignKey('users.id', ondelete="CASCADE"), primary_key=True),
    db.Column('place_id', db.String(36), db.ForeignKey('places.id', ondelete="CASCADE"), primary_key=True)
)

class User(BaseModel):
    __tablename__ = 'users'
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    
    places = db.relationship('Place', backref='user', lazy=True, cascade="all, delete-orphan")
    reviews = db.relationship('Review', backref='user', lazy=True, cascade="all, delete-orphan")
    bookings = db.relationship('Booking', backref='user', lazy=True, cascade="all, delete-orphan")
    
    favorites = db.relationship('Place', secondary=user_favorites, backref=db.backref('favorited_by', lazy=True))
    def __init__(self, first_name, last_name, email, password, is_admin=False, **kwargs):
        super().__init__(**kwargs)
        self.validate_user_data(first_name, last_name, email)
        
        if not password or not isinstance(password, str) or len(password) < 6:
            raise ValueError("Password must be a string with at least 6 characters")
            
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin
        self.hash_password(password)

    @staticmethod
    def validate_user_data(first_name, last_name, email):
        if not first_name or len(first_name) > 50: 
            raise ValueError("First name is required and max 50 chars")
        if not last_name or len(last_name) > 50: 
            raise ValueError("Last name is required and max 50 chars")
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not email or not re.match(email_regex, email): 
            raise ValueError("A valid email is required")

    def hash_password(self, password):
        """Hash password before storing it"""
        self.password = bcrypt.generate_password_hash(password).decode("utf-8")

    def verify_password(self, password):
        """Check whether a password matches with the stored hash"""
        return bcrypt.check_password_hash(self.password, password)

    def update(self, data):
        first_name = data.get('first_name', self.first_name)
        last_name = data.get('last_name', self.last_name)
        email = data.get('email', self.email)
        
        self.validate_user_data(first_name, last_name, email)
        
        allowed_data = {key: value for key, value in data.items() if key in {"first_name", "last_name", "email"}}
        
        if "first_name" in allowed_data:
            allowed_data["first_name"] = allowed_data["first_name"].strip()
        if "last_name" in allowed_data:
            allowed_data["last_name"] = allowed_data["last_name"].strip()
        if "email" in allowed_data:
            allowed_data["email"] = allowed_data["email"].strip().lower()
            
        super().update(allowed_data)

    def to_dict(self):
        """Return public data of user but without password"""
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email
        }