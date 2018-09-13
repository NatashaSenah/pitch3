from . import db
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from . import login_manager
from datetime import datetime
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(UserMixin,db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(255),index = True)
    email = db.Column(db.String(255),unique = True,index = True)
    role_id = db.Column(db.Integer,db.ForeignKey('roles.id'))
    bio = db.Column(db.String(255))
    profile_pic_path = db.Column(db.String())
    password_secure = db.Column(db.String(255))
    reviews = db.relationship('Review',backref = 'user',lazy = "dynamic")

    pitch = db.relationship('Pitch',backref = 'user',lazy = "dynamic")
    @property
    def password(self):
        raise AttributeError('You cannot read the password attribute')

    @password.setter
    def password(self, password):
        self.password_secure = generate_password_hash(password)


    def verify_password(self,password):
            return check_password_hash(self.password_secure,password)
    def save_user(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return f'User {self.username}'
class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(255))
    users = db.relationship('User',backref = 'role',lazy="dynamic")


    def __repr__(self):
        return f'User {self.name}'
class Comment(db.Model):

    __tablename__ = 'reviews'
    id = db.Column(db.Integer,primary_key = True)
    pitch_title = db.Column(db.String(255),index = True)
    posted = db.Column(db.DateTime,default=datetime.utcnow)
    user_id = db.Column(db.Integer,db.ForeignKey("users.id"))
    def save_review(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_reviews(cls,id):
        reviews = Review.query.filter_by(pitch_id=id).all()
        return reviews
class Pitch(db.Model):
    __tablename__ = 'pitches'
    id =db.Column(db.Integer,primary_key=True)
    pitch_content =db.Column(db.String())
    pitch_category =db.Column(db.String(255))
    user_id= db.Column(db.Integer,db.ForeignKey('users.id'))


    def save_pitch(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_pitch(cls,id):
        pitches = Pitch.query.filter_by(id=id).all()
        return pitches
    @classmethod
    def get_all_pitches(cls):
        pitches =Pitch.query.order_by('-id').all()
        return pitches
    @classmethod
    def get_category(cls,cat):
        category =Pitch.query.filter_by(pitch_category=cat).order_by('-id').all()
        return category

class Comment(db.Model):
   __tablename__ = 'comments'

   id = db.Column(db.Integer, primary_key=True)
   comment_content = db.Column(db.String())
   pitch_id = db.Column(db.Integer)
   user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

   def save_comment(self):
       db.session.add(self)
       db.session.commit()

   @classmethod
   def get_comments(cls, id):
       comments = Comment.query.filter_by(pitch_id=id).all()
       return comments


class UpVote(db.Model):
   __tablename__ = 'upvotes'

   id = db.Column(db.Integer, primary_key=True)
   id_user = db.Column(db.Integer, db.ForeignKey('users.id'))
   pitch_id = db.Column(db.Integer)

   def save_vote(self):
       db.session.add(self)
       db.session.commit()

   @classmethod
   def get_votes(cls, id):
       upvote = UpVote.query.filter_by(pitch_id=id).all()
       return upvote

   def __repr__(self):
       return f'{self.id_user}:{self.pitch_id}'


class DownVote(db.Model):
   __tablename__ = 'downvotes'

   id = db.Column(db.Integer, primary_key=True)
   id_user = db.Column(db.Integer, db.ForeignKey('users.id'))
   pitch_id = db.Column(db.Integer)

   def save_vote(self):
       db.session.add(self)
       db.session.commit()

   @classmethod
   def get_downvotes(cls, id):
       downvote = DownVote.query.filter_by(pitch_id=id).all()
       return downvote

   def __repr__(self):
       return f'{self.id_user}:{self.pitch_id}'


class PhotoProfile(db.Model):
   __tablename__ = 'profile_photos'

   id = db.Column(db.Integer, primary_key=True)
   pic_path = db.Column(db.String())
   user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
