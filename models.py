from app import db, app
from flask_login import UserMixin
from flask_jwt_extended import create_access_token
from datetime import timedelta
from werkzeug.security import check_password_hash, generate_password_hash
import sys

from app import login_manager


class Task(db.Model):
    __tablename__ = "tasks"
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship("User", backref="tasks")

    def __init__(self, *args, **kwargs):
        super(Task, self).__init__(*args, **kwargs)

    def __repr__(self):
        return '<Post id: {}, description: {}, user id: {}>'.format(self.id, self.description, self.user_id)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
        return self.id

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
        return 1


class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(128), nullable=False, unique=True)
    pas = db.Column(db.String(256), nullable=False)

    def __init__(self, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)
        self.pas = generate_password_hash(kwargs['pas'])

    def __repr__(self):
        return '<User id: {}, login: {}, pas: {}>'.format(self.id, self.login, self.pas)

    @classmethod
    def authenticate(cls, login, pas):
        user = cls.query.filter(cls.login == login).first()
        if (user is None):
            return 0
        if (not check_password_hash(user.pas, pas)):
            return 1
        return user

    def get_token(self, expire_time=24):
        expire_delta = timedelta(expire_time)
        token = create_access_token(
            identity=self.login, expires_delta=expire_delta)
        return token

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
        return 'User successfully added ' + self.login
