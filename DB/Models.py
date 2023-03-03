from cfg import *
from slugify import slugify
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length

class CommentForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=30)])
    email = StringField('Email', validators=[DataRequired(), Length(min=2, max=50)])
    body = TextAreaField('Comment', validators=[DataRequired()])
    submit = SubmitField('Post Comment')
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