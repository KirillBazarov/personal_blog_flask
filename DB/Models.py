from cfg import *
from sqlalchemy import event
from slugify import slugify

class Post(db.Model):
    __tablename__ = 'posts_slug'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), unique=True,nullable=False)
    slug = db.Column(db.String(50), unique=True, nullable=False)

@event.listens_for(Post, 'before_insert')
def generate_slug(mapper, connection, target):
    target.slug = slugify(target.title)
