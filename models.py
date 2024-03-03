# models.py

from app import db

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    isbn = db.Column(db.String(20), unique=True, nullable=False)
    author = db.Column(db.String(100), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    length = db.Column(db.Integer, nullable=False)
    hardcover = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<Book {self.title}>'
