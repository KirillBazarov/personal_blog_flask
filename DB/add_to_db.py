from Models import Post
from cfg import *

posts = [
    Post(title='Заголовок 1', url='https://example.com/1'),
    Post(title='Заголовок 2', url='https://example.com/2')
]

db.session.add_all(posts)
db.session.commit()