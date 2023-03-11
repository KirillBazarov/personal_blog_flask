from cfg import *
from Models import *

posts = [
    Post(title='3аыфвавфыFsadf',content="ну тут меньшу 50 символов",user_id = 2),
]

# users = [
#     User(name='kirill',content="ну тут меньшу 50 символов",user_id = 1),
# ]
# id = db.Column(db.Integer, primary_key=True)
# content = db.Column(db.String(250))
# user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
# post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))

# comment = [
#     Comment(content="второй комент для превого поста от первого юзера",user_id = 1,post_id= 1),
# ]

with app.app_context():
    # db.session.add_all(users)
    db.session.add_all(posts)
    db.session.commit()
