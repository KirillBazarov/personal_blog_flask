from cfg import *
from Models import Post
#
#
# posts = [
#     Post(title='Заголовок 1'),
#     Post(title='Заголовок 2')
# ]
#
# with app.app_context():
#     db.session.add_all(posts)
#     db.session.commit()

# Создание новой записи



# Сохранение изменений в базе данных
with app.app_context():
    post2 = Post(title='Заголовок 2')
    db.session.add(post2)
    db.session.commit()
