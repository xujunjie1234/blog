
from datetime import datetime

from flask_login import UserMixin
from werkzeug.security import generate_password_hash,check_password_hash
from myblog.extensions import db


class Admin(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    password_hash = db.Column(db.String(500))
    blog_title = db.Column(db.String(100))
    body = db.Column(db.Text)
    html = db.Column(db.Text)
    timestamp = db.Column(db.DateTime,default=datetime.timestamp(datetime.now()),index=True)
    

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def validate_password_hash(self, password):
        return check_password_hash(self.password_hash, password)


class Category(db.Model):
    __tablename__ = "category"
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(100))
    posts = db.relationship("Post",back_populates="category",cascade='all,delete-orphan')

    def delete(self):
        default_category = Category.query.get(1)
        posts = self.posts[:]
        for post in posts:
            post.category = default_category
        db.session.delete(self)
        db.session.commit()


class Post(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(100))
    body = db.Column(db.Text)
    html = db.Column(db.Text)
    timestamp = db.Column(db.DateTime,default=datetime.timestamp(datetime.now()),index=True)
    can_comment = db.Column(db.Boolean,default=True)
    view = db.Column(db.Integer,default=0)
    like = db.Column(db.Integer,default=0)

    category_id = db.Column(db.Integer,db.ForeignKey('category.id'))
    category = db.relationship('Category',back_populates='posts')

    comments = db.relationship('Comment',back_populates='post',cascade='all,delete-orphan')


class Comment(db.Model):
    __tablename__ = 'comment'
    id = db.Column(db.Integer,primary_key=True)
    author = db.Column(db.String(100))
    email = db.Column(db.String(254))
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime,default=datetime.timestamp(datetime.now()),index=True)
    show = db.Column(db.Boolean, default=True)
    to = db.Column(db.String(100))
    like = db.Column(db.Integer)

    post_id = db.Column(db.Integer,db.ForeignKey('post.id'))
    post = db.relationship('Post',back_populates='comments')


    replies = db.relationship('Comment',back_populates='replied',cascade='all,delete-orphan') #全部子评论

    replied_id = db.Column(db.Integer,db.ForeignKey('comment.id'))    
    replied = db.relationship('Comment',back_populates='replies',remote_side=[id]) 


class News(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    author = db.Column(db.String(50))
    post_id = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime,default=datetime.timestamp(datetime.now()),index=True)
    body = db.Column(db.Text)
    reviewed = db.Column(db.Boolean,default=False)