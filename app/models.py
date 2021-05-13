from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from flask_login import UserMixin
from app import login


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Post(db.Model):  # Модель таблицы где хранятся список дел... Потом надо переименовать в Task!
    id = db.Column(db.Integer, primary_key=True)
    mission = db.Column(db.String(255))  # body
    timestamp_start = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    due_date = db.Column(db.DateTime, index=True, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Task {}>'.format(self.mission)


@login.user_loader
def load_user(_id):  # _id - Идентификатор пользователя
    return User.query.get(int(_id))
