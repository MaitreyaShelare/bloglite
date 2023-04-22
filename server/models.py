from datetime import datetime, timedelta
from __init__ import db
from __init__ import ma

import pytz
from marshmallow import fields

tz = pytz.timezone('Asia/Kolkata')

user_followers = db.Table('user_followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('timestamp', db.DateTime, default=datetime.now(tz))
)

user_likes = db.Table('user_likes',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('blog_id', db.Integer, db.ForeignKey('blog.id'), primary_key=True),
    db.Column('timestamp', db.DateTime, default=datetime.now(tz))
)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    dp = db.Column(db.String, nullable=True)
    dp_mimetype = db.Column(db.String, nullable=True)
    posts = db.Column(db.Integer, default=0)
    likes = db.relationship('Like', backref='user', lazy=True)
    comments = db.relationship('Comment', backref='user', lazy=True)
    
    followed_users = db.relationship(
        'User', secondary=user_followers,
        primaryjoin=(user_followers.c.follower_id == id),
        secondaryjoin=(user_followers.c.followed_id == id),
        backref=db.backref('followers_users', lazy='dynamic'), lazy='dynamic')
    
    liked_blogs = db.relationship(
        'Blog', secondary=user_likes,primaryjoin=(user_likes.c.user_id == id),lazy='dynamic')

    def follow(self, user):
     if not self.is_following(user):
            self.followed_users.append(user)
            db.session.commit()

    def unfollow(self, user):
        if self.is_following(user):
            self.followed_users.remove(user)
            db.session.commit()

    def is_following(self, user):
        return self.followed_users.filter(user_followers.c.followed_id == user.id).count()
    
    def like(self, blog):
        if not self.has_liked(blog):
            self.liked_blogs.append(blog)
            like = Like(user_id=self.id, blog_id=blog.id)
            db.session.add(like)
            db.session.commit()

    def unlike(self, blog):
        if self.has_liked(blog):
            self.liked_blogs.remove(blog)
            Like.query.filter_by(user_id=self.id,blog_id=blog.id).delete()
            db.session.commit()

    def has_liked(self, blog):
        return Like.query.filter(
            Like.user_id == self.id,
            Like.blog_id == blog.id
        ).count() > 0        

    # For Report
    def new_followers_past_month(self):
        count = (
        db.session.query(User)
        .join(user_followers, user_followers.c.followed_id == User.id)
        .filter(user_followers.c.follower_id == self.id)
        .filter(user_followers.c.timestamp > (datetime.now(tz) - timedelta(days=30)))
        .count()
        )
        return str(count)
    
    def new_following_past_month(self):
        count = (
            db.session.query(User)
            .join(user_followers, user_followers.c.follower_id == User.id)
            .filter(user_followers.c.followed_id == self.id)
            .filter(user_followers.c.timestamp > (datetime.now(tz) - timedelta(days=30)))
            .count()
        )
        return str(count)

    def blogs_posted_past_month(self):
        count = (
            db.session.query(Blog)
            .filter_by(user_id=self.id)
            .filter(Blog.timestamp > (datetime.now(tz) - timedelta(days=30)))
            .count()
        )
        return str(count)
    
    def blogs_liked_past_month(self):
        count = (
            db.session.query(Blog)
            .join(user_likes, user_likes.c.blog_id == Blog.id)
            .filter(user_likes.c.user_id == self.id)
            .filter(user_likes.c.timestamp > (datetime.now(tz) - timedelta(days=30)))
            .count()
        )
        return str(count)
    
    def blogs_commented_past_month(self):
        count = (
            db.session.query(Comment)
            .join(Blog)
            .filter(Comment.user_id == self.id)
            .filter(Comment.timestamp > (datetime.now(tz) - timedelta(days=30)))
            .count()
        )
        return str(count)


class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(255), nullable=False)
    photo = db.Column(db.String, nullable=False)
    photo_mimetype = db.Column(db.String, nullable=False)
    timestamp = db.Column(db.DateTime(timezone=True),default=datetime.now(tz))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref='blog')
    likes = db.relationship('Like', backref='blog', lazy=True)
    liked_by = db.relationship('User', secondary=user_likes,overlaps="liked_blogs", lazy='dynamic')
    comments = db.relationship('Comment', backref='blog', lazy=True)
    hidden = db.Column(db.Boolean, default=False)  

    @property
    def liked_by_users(self):
        return [like.user_id for like in self.likes]
        
    

class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    blog_id = db.Column(db.Integer, db.ForeignKey('blog.id'))



class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(255), nullable=False)
    timestamp = db.Column(db.DateTime(timezone=True),default=datetime.now(tz))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    blog_id = db.Column(db.Integer, db.ForeignKey('blog.id'))


class LikeSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Like
        include_relationships = True
        load_instance = True


class CommentSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Comment
        include_relationships = True
        load_instance = True

    server_time = fields.Method('get_server_time')

    def get_server_time(self, obj):
        tz = pytz.timezone('Asia/Kolkata')
        server_time = datetime.now(tz)
        server_time_str = server_time.strftime('%Y-%m-%dT%H:%M:%S.%f')
        return server_time_str
    
    user = ma.Nested('UserSchema', only=('id', 'name', 'dp', 'dp_mimetype'))    

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        include_relationships = True
        load_instance = True

    blogs = ma.Nested('BlogSchema', many=True, only=('id', 'text', 'timestamp'))
   

class BlogSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Blog
        include_relationships = True
        load_instance = True

    server_time = fields.Method('get_server_time')

    def get_server_time(self, obj):
        tz = pytz.timezone('Asia/Kolkata')
        server_time = datetime.now(tz)
        server_time_str = server_time.strftime('%Y-%m-%dT%H:%M:%S.%f')
        return server_time_str

    
    user = ma.Nested('UserSchema', only=('id', 'name', 'dp', 'dp_mimetype'))
   