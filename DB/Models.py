from cfg import *

class Post(db.Model):
    __tablename__ = 'test'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    url = db.Column(db.String(50), nullable=False)
