from cfg import *
from Models import *
#
#
# posts = [
#     Post(title='Заголовок 1'),
#     Post(title='Заголовок 2')
# ]
users = [
    User(name='fcas',email="cads@gmai.com", password="lol"),
]

with app.app_context():
    db.session.add_all(users)
    db.session.commit()

# Создание новой записи





# Сохранение изменений в базе данных
# with app.app_context():
#     post = Post(title='4', content="ну тут что-то важное про этот пост")
#     db.session.add(post)
#     db.session.commit()
