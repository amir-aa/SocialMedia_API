from peewee import SqliteDatabase, Model, CharField, ForeignKeyField, DateTimeField, fn
from datetime import datetime

# Create a SQLite database
db = SqliteDatabase('social_media.db')

# Define Peewee models
class User(Model):
    username = CharField(unique=True)

    class Meta:
        database = db

class Friendship(Model):
    user1 = ForeignKeyField(User, backref='friends')
    user2 = ForeignKeyField(User)

    class Meta:
        database = db

class Post(Model):
    user = ForeignKeyField(User, backref='posts')
    content = CharField()
    created_at = DateTimeField(default=datetime.now)

    class Meta:
        database = db

class Like(Model):
    user = ForeignKeyField(User)
    post = ForeignKeyField(Post, backref='likes')

    class Meta:
        database = db

class Comment(Model):
    user = ForeignKeyField(User)
    post = ForeignKeyField(Post, backref='comments')
    content = CharField()
    created_at = DateTimeField(default=datetime.now)

    class Meta:
        database = db

# Create tables
db.connect()
db.create_tables([User, Friendship, Post, Like, Comment])
