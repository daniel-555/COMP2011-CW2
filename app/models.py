from app import db
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.string(255))
    email = db.Column(db.String(100), unique=True)

    posts = db.relationship('Post', backref='author', lazy=True)
    comments = db.relationship('Comment', backref='commentor', lazy=True)
    likes = db.relationship('Like', backref='user', lazy=True)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    post_author = db.Column(db.Integer, db.ForeignKey('user.id'))

    content = db.Column(db.String(1000))
    created_at = db.Column(db.DateTime, default=datetime.now())

    comments = db.relationship('Comment', backref='post', lazy=True)
    likes = db.relationship('Like', backref='post', lazy=True)

class Comment:
    id = db.Column(db.Integer, primary_key=True)

    comment_creator = db.Column(db.Integer, db.ForeignKey('user.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))

    content = db.Column(db.String(200))
    

class Like:
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), primary_key=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True, nullable=False)

    liked_at = db.Column(db.DateTime(), default=datetime.now())


# Implement if there is time
# class Follower:
#     pass