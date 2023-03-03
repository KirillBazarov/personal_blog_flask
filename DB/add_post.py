from cfg import *


class PostTest(db.Model):
    __tablename__ = 'test'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    url = db.Column(db.String(50), nullable=False)


posts = [
    PostTest(title='Заголовок 1', url='https://example.com/1'),
    PostTest(title='Заголовок 2', url='https://example.com/2')
]

with app.app_context():
    db.session.add_all(posts)
    db.session.commit()
