# models.py

# from app import db

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import uuid 
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flask_login import LoginManager
from flask_marshmallow import Marshmallow 
import secrets

login_manager = LoginManager()
ma = Marshmallow()
db = SQLAlchemy()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)



class User(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    g_auth_verify = db.Column(db.Boolean, default = False)
    token = db.Column(db.String, default = '', unique = True )
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    

    # Initialization Method (Instance Method)
    def __init__(self, username='', email='', password='', token='', g_auth_verify=False):
        self.id = self.set_id()
        self.username = username
        self.email = email
        self.password = self.set_password(password)
        self.token = self.set_token(24)
        self.g_auth_verify = g_auth_verify

    # Instance Method to Generate Random String of Numbers / Letters
    def set_id(self):
        return str(uuid.uuid4())

    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)
        return self.pw_hash
    
    def check_password(self, password):
        is_valid = check_password_hash(self.password, password)

        return is_valid
    
    def set_token(self, length):
        return secrets.token_hex(length)

    def __repr__(self):
        return f'<User {self.username}>'
    

class Book(db.Model):

    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True)
    isbn = db.Column(db.Integer, unique=True)
    author = db.Column(db.String, unique=True, nullable=False)
    title = db.Column(db.String, nullable=False)
    length = db.Column(db.Integer, nullable=False)
    hardcover = db.Column(db.Boolean, default = False)
    
    def __init__(self, id='', isbn='', author='', title='', length='', hardcover=False):
        self.id = id
        self.isbn = isbn
        self.author = author
        self.title = title
        self.length = length
        self.hardcover = hardcover