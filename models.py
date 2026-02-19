from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    movies = db.relationship('Movie', backref='user', lazy=True)


class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    publication_year = db.Column(db.Integer)
    cover = db.Column(db.String)

    # Link Movie to User
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
