from cfg import *
from Models import *

users = [
    User(name='fcas',email="cads@gmai.com", password="lol"),
]

with app.app_context():
    db.session.add_all(users)
    db.session.commit()
