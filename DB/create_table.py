from Models import *


with app.app_context():
    db.create_all()
    db.session.commit()

