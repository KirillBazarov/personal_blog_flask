import datetime

from cfg import *



# подтверждаем транзакцию

with app.app_context():
    db.create_all()
    db.session.commit()

