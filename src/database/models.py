import uuid

from werkzeug.security import generate_password_hash

from src import db


class Book(db.Model):
    __tablename__ = 'books'

    def __init__(self, title, release_date, description, distributed_by, length, rating):
        self.title = title
        self.release_date = release_date
        self.description = description
        self.distributed_by = distributed_by
        self.length = length
        self.rating = rating
        self.uid = str(uuid.uuid4())

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    release_date = db.Column(db.Date, index=True, nullable=False)
    uid = db.Column(db.String(36), unique=True)
    description = db.Column(db.Text)
    distributed_by = db.Column(db.String(64), nullable=False)
    length = db.Column(db.Integer)
    rating = db.Column(db.Float)
    author = db.Column(db.Integer, db.ForeignKey('authors.id'))

    def __repr__(self):
        return f'Book: {self.title}, {self.uid}, {self.rating}, {self.distributed_by}, {self.release_date}'


class Author(db.Model):
    __tablename__ = 'authors'

    def __init__(self, name, birthday, is_active=None):
        self.name = name
        self.birthday = birthday
        self.is_active = is_active

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    birthday = db.Column(db.Date, index=True, nullable=False)
    books = db.relationship('Book', backref='book', foreign_keys=[Book.author])
    is_active = db.Column(db.Integer, default=False)

    def __repr__(self):
        return f'Author: {self.name}, {self.birthday}'


class User(db.Model):
    __tablename__ = 'users'

    def __init__(self, username, email, password, is_admin=False):
        self.username = username
        self.email = email
        self.password = generate_password_hash(password)
        self.is_admin = is_admin
        self.uid = str(uuid.uuid4())

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(64), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    uid = db.Column(db.String(36), unique=True)

    def __repr__(self):
        return f'User: {self.username}, {self.email}, {self.uid}, {self.is_admin}'

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_uid(cls, uid):
        return cls.query.filter_by(uid=uid).first()
