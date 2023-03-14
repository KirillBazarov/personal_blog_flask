from datetime import datetime
from flask import url_for
from slugify import slugify
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash
from cfg import *


class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), unique=True, nullable=False)
    content = db.Column(db.String(250), nullable=False)
    slug = db.Column(db.String(50), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, title, content, user_id):
        self.title = title
        self.slug = slugify(title)
        self.content = content
        self.user_id = user_id

    @classmethod
    def get_by_slug(cls, slug):
        post = Post.query.filter_by(slug=slug).first()
        return post

    @classmethod
    def delete_post(self,slug):
        post_to_delete = Post.query.filter_by(slug=slug).first_or_404()
        comments_to_delete = Comment.query.filter_by(post_id=post_to_delete.id).all()
        for comment in comments_to_delete:
            db.session.delete(comment)
        db.session.delete(post_to_delete)
        db.session.commit()



class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(50), unique=True)
    password_hash = db.Column(db.String(128))
    avatar = db.Column(db.LargeBinary, nullable=True)

    posts = relationship('Post', backref='author')
    comments = relationship('Comment', backref='author')

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password_hash = generate_password_hash(password)
        self.avatar = None

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    def verifyExt(self, filename):
        """
        Verify if the file has an allowed extension.
        """
        allowed_extensions = {'jpg', 'jpeg', 'png', 'gif'}
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in allowed_extensions

    def update_avatar(avatar, user_id):
        user = User.query.filter_by(id=user_id).first()
        user.avatar = avatar.read()
        db.session.commit()

        return 'Avatar updated successfully'

    def getAvatar(self, app):
        img = None
        if not self.avatar:
            try:
                with app.open_resource(app.root_path + url_for('static', filename='images/default.png'), "rb") as f:
                    img = f.read()
            except FileNotFoundError as e:
                print("Не найден аватар по умолчанию: " + str(e))
        else:
            img = self.avatar
        return img

    @classmethod
    def add_user(cls,name, email, password):
        new_user = cls(name=name, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        return new_user

    def count_user_posts(id):
        user_count = Post.query.filter_by(user_id=id).count()
        return user_count

class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(250))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))

    comments = relationship('Post', backref='comm')

    @classmethod
    def add_comment(cls, content, post_id, user_id):
        comment = cls(content=content, post_id=post_id, user_id=user_id)
        db.session.add(comment)
        db.session.commit()


    @classmethod
    def delete_comment_id(cls, id):
        comment = cls.query.filter_by(id=id).first()
        db.session.delete(comment)
        db.session.commit()

class PostLikes(db.Model):
    __tablename__ = 'post_likes'

    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    post_likes = relationship('Post', backref='likes')