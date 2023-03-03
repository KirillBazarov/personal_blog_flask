from slugify import slugify

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

