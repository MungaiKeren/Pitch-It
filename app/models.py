from . import db
from . import login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash,check_password_hash
from datetime import datetime


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(UserMixin,db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(255),index=True)
    email = db.Column(db.String(255),unique = True,index = True)
    role_id = db.Column(db.Integer,db.ForeignKey('roles.id'))
    bio = db.Column(db.String(255))
    profile_pic_path = db.Column(db.String())
    pass_secure = db.Column(db.String(255))

    @property
    def password(self):
        raise AttributeError('You cannot read the password attribute')

    @password.setter
    def password(self, password):
        self.pass_secure = generate_password_hash(password)


    def verify_password(self,password):
        return check_password_hash(self.pass_secure,password)
    
    def __repr__(self):
        return f'User {self.username}'


class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(255))
    users = db.relationship('User',backref = 'role',lazy="dynamic")

    def __repr__(self):
        return f'User {self.name}'


class Pitch(db.Model):
    __tablename__='pitches'

    id=db.Column(db.Integer,primary_key=True)
    upvotes = db.Column(db.Integer)
    downvotes = db.Column(db.Integer)
    title = db.Column(db.String(255))
    pitch = db.Column(db.String(255))
    posted = db.Column(db.DateTime,default=datetime.utcnow)
    user_id = db.Column(db.Integer,db.ForeignKey("users.id"))
    comments = db.relationship('Comment',backref='user',lazy='dynamic')

    def save_pitch():
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_pitches(cls):
        pitches = Pitch.query.order_by(Pitch.posted.desc()).all()
        return pitches

class Comment(db.Model):
    __tablename__='comments'
    id = db.Column(db.Integer,primary_key=True)
    comment = db.Column(db.String(255))
    pitch_id = db.Column(db.Integer,db.ForeignKey("pitches.id"))
    posted = db.Column(db.DateTime,default=datetime.utcnow)

    def save_comment():
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_comments(cls):
        comments = Comment.query.order_by(Comment.posted.desc()).all()
        return comments