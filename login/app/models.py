from werkzeug.security import generate_password_hash, check_password_hash
from . import db, lm
from flask_login import UserMixin

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(16), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    cert = db.Column(db.String(128))
    logged = db.Column(db.Integer)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def register(username, password, cert):
        user = User(username=username, cert=cert, logged=0) 
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return user

    def __repr__(self):
        return '<User {0}>'.format(self.username)

def logCert():
    __tablename__ = 'users'
    user = User.query.filter_by(username=current_user.username).first()
    user.logged = 1
    db.session.commit()

@lm.user_loader
def load_user(id):
    return User.query.get(int(id))
