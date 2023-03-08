from flask import url_for
from slugify import slugify
from werkzeug.security import generate_password_hash, check_password_hash

from cfg import *


class Post(db.Model):
    __tablename__ = 'posts_slug'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), unique=True, nullable=False)
    content = db.Column(db.String(50), nullable=False)
    slug = db.Column(db.String(50), unique=True, nullable=False)

    def __init__(self, title, content):
        self.title = title
        self.slug = slugify(title)
        self.content = content

    @classmethod
    def get_by_slug(cls, slug):
        return cls.query.filter_by(slug=slug).first()


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(50), unique=True)
    password_hash = db.Column(db.String(128))
    avatar =  db.Column(db.LargeBinary, nullable=True)

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
        # Получаем данные POST-запроса


        # Получаем пользователя из базы данных
        user = User.query.filter_by(id=user_id).first()

        # Обновляем аватарку пользователя
        user.avatar = avatar.read()

        # Сохраняем изменения в базе данных
        db.session.commit()

        return 'Avatar updated successfully'

    def getAvatar(self, app):
        img = None
        if not self.avatar:
            try:
                with app.open_resource(app.root_path + url_for('static', filename='images/default.png'), "rb") as f:
                    img = f.read()
            except FileNotFoundError as e:
                print("Не найден аватар по умолчанию: "+str(e))
        else:
            img = self.avatar
        return img