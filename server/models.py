#IMPORTS
from sqlalchemy.sql import func
from __init__ import db
from __init__ import ma


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(20))
    name = db.Column(db.String(40))
    #Parent to List
    lists = db.relationship('List', cascade="all, delete")


class List(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    # Child of User, Parent of Task
    tasks = db.relationship('Task', cascade="all, delete")
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20))
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    date_completed = db.Column(db.DateTime(timezone=True))
    deadline = db.Column(db.DateTime(timezone=True))
    status = db.Column(db.Boolean(), default=False )
    deadline_passed = db.Column(db.Boolean(), default=False )
    #Child of List
    list_id = db.Column(db.Integer, db.ForeignKey('list.id'))    


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User

class ListSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = List

class TaskSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Task        