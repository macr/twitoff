from flask_sqlalchemy import SQLAlchemy 
from sqlalchemy.sql import func
import datetime
db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    username = db.Column(db.String(140), unique=True)
    name = db.Column(db.String(240), unique=True)

    def __repr__(self):
        return f'<User {self.username}>'

class Tweet(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    user_id = db.Column(db.BigInteger,
                        db.ForeignKey('user.id'),
                        nullable=False)
    user = db.relationship(
        'User',
        backref=db.backref('tweets', lazy='dynamic'))
    text = db.Column(db.Unicode(500), nullable=False)
    embeddings = db.Column(db.PickleType, nullable=False)

    def __repr__(self):
        return f'<Tweet {self.text}>'
        