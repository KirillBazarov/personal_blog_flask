from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost:3306/flask'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB max upload size
app.config['SECRET_KEY'] = 'your_secret_key_here'
app.config['UPLOAD_FOLDER'] = 'uploads'


app.config["RECAPTCHA_PUBLIC_KEY"] = "6LcN8NkkAAAAAJAvEFK3F9k-15J0u5mBMAezgCCZ"
app.config["RECAPTCHA_PRIVATE_KEY"] = "6LcN8NkkAAAAAORCvkhjbCWA_s8Kn0iQ6DbXSo8G"


login_manager = LoginManager()
login_manager.init_app(app)


db = SQLAlchemy(app)
