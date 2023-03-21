from datetime import datetime
from __init__ import db
from __init__ import ma


# Define the association table for the many-to-many relationship between users for following
user_followers = db.Table('user_followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'), primary_key=True)
)

# Define the association table for the many-to-many relationship between users and blogs for liking
user_likes = db.Table('user_likes',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('blog_id', db.Integer, db.ForeignKey('blog.id'), primary_key=True)
)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    dp = db.Column(db.LargeBinary, nullable=False)
    followers = db.Column(db.Integer, default=0)
    posts = db.Column(db.Integer, default=0)
    likes = db.relationship('Like', backref='user', lazy=True)
    comments = db.relationship('Comment', backref='user', lazy=True)
    
    followed_users = db.relationship(
        'User', secondary=user_followers,
        primaryjoin=(user_followers.c.follower_id == id),
        secondaryjoin=(user_followers.c.followed_id == id),
        backref=db.backref('followers_users', lazy='dynamic'), lazy='dynamic')
    
    def __repr__(self):
        return f"User('{self.name}', '{self.email}', '{self.followers}', '{self.posts}', '{self.dp}')"


class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(255), nullable=False)
    photo = db.Column(db.LargeBinary, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref='blogs')
    likes = db.relationship('Like', backref='blog', lazy=True)
    comments = db.relationship('Comment', backref='blog', lazy=True)
    hidden = db.Column(db.Boolean, default=False)  

    def __repr__(self):
        return f"Blog('{self.text}', '{self.timestamp}', '{self.hidden}', '{self.photo}')"

class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    blog_id = db.Column(db.Integer, db.ForeignKey('blog.id'), nullable=False)

    def __repr__(self):
        return f"Like('{self.id}', '{self.user_id}', '{self.blog_id}')"


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(255), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    blog_id = db.Column(db.Integer, db.ForeignKey('blog.id'), nullable=False)

    def __repr__(self):
        return f"Comment('{self.text}', '{self.timestamp}', '{self.user_id}', '{self.blog_id}')"


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User

    blogs = ma.Nested('BlogSchema', many=True, only=('id', 'text', 'timestamp'))
    likes = ma.Nested('LikeSchema', many=True, only=('id', 'user_id', 'blog_id'))
    comments = ma.Nested('CommentSchema', many=True, only=('id', 'text', 'timestamp', 'user_id', 'blog_id'))


class BlogSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Blog

    user = ma.Nested('UserSchema', only=('id', 'name'))
    likes = ma.Nested('LikeSchema', many=True, only=('id', 'user_id', 'blog_id'))
    comments = ma.Nested('CommentSchema', many=True, only=('id', 'text', 'timestamp', 'user_id', 'blog_id'))


class LikeSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Like


class CommentSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Comment


# 4
# from datetime import datetime
# from __init__ import db
# from __init__ import ma


# # Define the association table for the many-to-many relationship between users for following
# user_followers = db.Table('user_followers',
#     db.Column('follower_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
#     db.Column('followed_id', db.Integer, db.ForeignKey('user.id'), primary_key=True)
# )

# # Define the association table for the many-to-many relationship between users and blogs for liking
# user_likes = db.Table('user_likes',
#     db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
#     db.Column('blog_id', db.Integer, db.ForeignKey('blog.id'), primary_key=True)
# )

# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(20), nullable=False)
#     email = db.Column(db.String(120), unique=True, nullable=False)
#     password = db.Column(db.String(60), nullable=False)
#     followers = db.Column(db.Integer, default=0)
#     posts = db.Column(db.Integer, default=0)
#     likes = db.relationship('Like', backref='user', lazy=True)
#     comments = db.relationship('Comment', backref='user', lazy=True)
    
#     def __repr__(self):
#         return f"User('{self.name}', '{self.email}', '{self.followers}', '{self.posts}')"


# class Blog(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(100), nullable=False)
#     caption = db.Column(db.String(255))
#     image_url = db.Column(db.String(255), nullable=False)
#     timestamp = db.Column(db.DateTime, default=datetime.utcnow)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
#     user = db.relationship('User', backref='blogs')
#     likes = db.relationship('Like', backref='blog', lazy=True)
#     comments = db.relationship('Comment', backref='blog', lazy=True)
#     hidden = db.Column(db.Boolean, default=False)  

#     def __repr__(self):
#         return f"Blog('{self.title}', '{self.caption}', '{self.image_url}', '{self.timestamp}', '{self.hidden}')"

# class Like(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
#     blog_id = db.Column(db.Integer, db.ForeignKey('blog.id'), nullable=False)

#     def __repr__(self):
#         return f"Like('{self.id}', '{self.user_id}', '{self.blog_id}')"


# class Comment(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     text = db.Column(db.String(255), nullable=False)
#     timestamp = db.Column(db.DateTime, default=datetime.utcnow)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
#     blog_id = db.Column(db.Integer, db.ForeignKey('blog.id'), nullable=False)

#     def __repr__(self):
#         return f"Comment('{self.text}', '{self.timestamp}', '{self.user_id}', '{self.blog_id}')"


# class UserSchema(ma.SQLAlchemyAutoSchema):
#     class Meta:
#         model = User

#     blogs = ma.Nested('BlogSchema', many=True, only=('id', 'title', 'caption', 'image_url', 'timestamp'))
#     likes = ma.Nested('LikeSchema', many=True, only=('id', 'user_id', 'blog_id'))
#     comments = ma.Nested('CommentSchema', many=True, only=('id', 'text', 'timestamp', 'user_id', 'blog_id'))


# class BlogSchema(ma.SQLAlchemyAutoSchema):
#     class Meta:
#         model = Blog

#     user = ma.Nested('UserSchema', only=('id', 'name'))
#     likes = ma.Nested('LikeSchema', many=True, only=('id', 'user_id', 'blog_id'))
#     comments = ma.Nested('CommentSchema', many=True, only=('id', 'text', 'timestamp', 'user_id', 'blog_id'))


# class LikeSchema(ma.SQLAlchemyAutoSchema):
#     class Meta:
#         model = Like


# class CommentSchema(ma.SQLAlchemyAutoSchema):
#     class Meta:
#         model = Comment


#3 
# from datetime import datetime
# from __init__ import db
# from __init__ import ma

# class Blog(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(100), nullable=False)
#     caption = db.Column(db.String(255))
#     image_url = db.Column(db.String(255), nullable=False)
#     timestamp = db.Column(db.DateTime, default=datetime.utcnow)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
#     user = db.relationship('User', backref='blogs')

#     def __repr__(self):
#         return f"Blog('{self.title}', '{self.caption}', '{self.image_url}', '{self.timestamp}')"

# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(20), nullable=False)
#     email = db.Column(db.String(120), unique=True, nullable=False)
#     password = db.Column(db.String(60), nullable=False)
#     followers = db.Column(db.Integer, default=0)
#     posts = db.Column(db.Integer, default=0)

#     def __repr__(self):
#         return f"User('{self.name}', '{self.email}', '{self.followers}', '{self.posts}')"

# class BlogSchema(ma.SQLAlchemyAutoSchema):
#     class Meta:
#         model = Blog

#     user = ma.Nested(lambda: UserSchema(only=('id', 'name')), dump_only=True)

# class UserSchema(ma.SQLAlchemyAutoSchema):
#     class Meta:
#         model = User

#     blogs = ma.Nested(lambda: BlogSchema(only=('id', 'title', 'caption', 'image_url', 'timestamp')), many=True, dump_only=True)


# # Import necessary modules 2
# from datetime import datetime
# from __init__ import db
# from __init__ import ma

# # Define the Blog model
# class Blog(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(100), nullable=False)
#     caption = db.Column(db.String(255))
#     image_url = db.Column(db.String(255), nullable=False)
#     timestamp = db.Column(db.DateTime, default=datetime.utcnow)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
#     user = db.relationship('User', backref='blogs')

#     def __repr__(self):
#         return f"Blog('{self.title}', '{self.caption}', '{self.image_url}', '{self.timestamp}')"

# # Define the User model
# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(20), nullable=False)
#     email = db.Column(db.String(120), unique=True, nullable=False)
#     password = db.Column(db.String(60), nullable=False)
#     followers = db.Column(db.Integer, default=0)
#     posts = db.Column(db.Integer, default=0)

#     def __repr__(self):
#         return f"User('{self.name}', '{self.email}', '{self.followers}', '{self.posts}')"

# # Define the Blog schema
# class BlogSchema(ma.SQLAlchemySchema):
#     class Meta:
#         model = Blog
#         fields = ('id', 'title', 'caption', 'image_url', 'timestamp', 'user_id')

#     user = ma.Nested('UserSchema', only=('id', 'name'))

# # Define the User schema
# class UserSchema(ma.SQLAlchemySchema):
#     class Meta:
#         model = User
#         fields = ('id', 'name', 'email', 'followers', 'posts')

#     blogs = ma.Nested(BlogSchema, many=True, only=('id', 'title', 'caption', 'image_url', 'timestamp'))



# #IMPORTS 1
# from sqlalchemy.sql import func
# from __init__ import db
# from __init__ import ma


# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     email = db.Column(db.String(50), unique=True)
#     password = db.Column(db.String(20))
#     name = db.Column(db.String(40))
#     #Parent to List
#     lists = db.relationship('List', cascade="all, delete")


# class List(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(20))
#     date = db.Column(db.DateTime(timezone=True), default=func.now())
#     # Child of User, Parent of Task
#     tasks = db.relationship('Task', cascade="all, delete")
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


# class Task(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(20))
#     data = db.Column(db.String(10000))
#     date = db.Column(db.DateTime(timezone=True), default=func.now())
#     date_completed = db.Column(db.DateTime(timezone=True))
#     deadline = db.Column(db.DateTime(timezone=True))
#     status = db.Column(db.Boolean(), default=False )
#     deadline_passed = db.Column(db.Boolean(), default=False )
#     #Child of List
#     list_id = db.Column(db.Integer, db.ForeignKey('list.id'))    


# class UserSchema(ma.SQLAlchemyAutoSchema):
#     class Meta:
#         model = User

# class ListSchema(ma.SQLAlchemyAutoSchema):
#     class Meta:
#         model = List

# class TaskSchema(ma.SQLAlchemyAutoSchema):
#     class Meta:
#         model = Task        