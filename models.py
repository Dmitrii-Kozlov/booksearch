from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class Users(db.Model):
    __tablename__ = "users1"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)

class Books(db.Model):
    __tablename__ = "books1"
    id = db.Column(db.Integer, primary_key=True)
    isbn = db.Column(db.String, nullable=False)
    title = db.Column(db.String, nullable=False)
    author = db.Column(db.String, nullable=False)
    year = db.Column(db.Integer, nullable=False)

class Reviews(db.Model):
    __tablename__ = "reviews1"
    id = db.Column(db.Integer, primary_key=True)
    review = db.Column(db.String)
    book_id = db.Column(db.Integer, db.ForeignKey("books1.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users1.id"), nullable=False)
    review_value = db.Column(db.Integer, nullable=False)
    books = db.relationship("Books", backref="reviews", lazy=True)
    users = db.relationship("Users", backref="reviews", lazy=True)