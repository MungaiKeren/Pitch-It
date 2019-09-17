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
    title = db.Column(db.String(255))
    category = db.Column(db.String(255),nullable=False)
    pitch = db.Column(db.String(255))
    posted = db.Column(db.DateTime,default=datetime.utcnow)
    user_id = db.Column(db.Integer,db.ForeignKey("users.id"),nullable=False)
    # relationships
    comments = db.relationship('Comment',backref='pitch',lazy='dynamic')
    upvotes = db.relationship('Upvote',backref='pitch',lazy='dynamic')
    

    def save_pitch():
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_pitches(cls):
        pitches = Pitch.query.order_by(Pitch.posted.desc()).all()
        return pitches

    def __repr__(self):
        return f'Pitch {self.pitch}'
# upvotes model
class Upvote(db.Model):
    __tablename__='upvotes'

    id= db.Column(db.Integer,primary_key=True)
    upvote=db.Column(db.Integer,default=1)
    pitch_id = db.Column(db.Integer,db.ForeignKey("pitches.id"))
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'),nullable=False)

    def save_upvote():
        db.session.save(self)
        db.session.commit()

    def total_upvotes():
        upvote_pitch = Upvote(user=current_user,pitch_id=id)
        upvote_pitch.save_upvote()

    @classmethod
    def get_upvotes(cls,id):
        upvote = Upvote.query.filter_by(pitch_id=id).all()
        return upvote

    @classmethod
    def get_all_upvotes(cls,pitch_id):
        upvotes = Upvote.query.order_by('id').all()
        return upvotes

    def __repr__(self):
        return f'{self.user_id}:{self.pitch_id}'

# down votes model
class DownVote(db.Model):
    __tablename__='downvotes'

    id = db.Column(db.Integer,primary_key=True)
    downvote=db.Column(db.Integer,default=1)
    pitch_id = db.Column(db.Integer,db.ForeignKey("pitches.id"))
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'),nullable=False)

    def save_downvote():
        db.session.save(self)
        db.session.commit()

    def total_downvotes():
        downvote_pitch= DownVote(user=current_user,pitch_id=id)
        downvote_pitch.save_downvote()

    @classmethod
    def get_downvotes(cls,id):
        downvote=DownVote.query.filter_by(pitch_id=id).all()
        return downvote

    @classmethod
    def get_all_downvotes(cls,id):
        downvotes = DownVote.query.order_by('id').all()
        return downvotes

    def __repr__(self):
        return f'{self.user_id}:{self.pitch_id}'

# comment model
class Comment(db.Model):
    __tablename__='comments'
    id = db.Column(db.Integer,primary_key=True)
    comment = db.Column(db.String(255))
    pitch_id = db.Column(db.Integer,db.ForeignKey("pitches.id"))
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'),nullable=False)
    posted = db.Column(db.DateTime,default=datetime.utcnow)

    def save_comment():
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_comments(cls):
        comments = Comment.query.order_by(Comment.posted.desc()).all()
        return comments

    def __repr__(self):
        return f'Comment id: {self.id} comment : {self.comment}'

