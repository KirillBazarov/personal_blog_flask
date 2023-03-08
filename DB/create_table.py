from Models import *


with app.app_context():
    # db.drop_all()
    db.create_all()
    db.session.commit()

