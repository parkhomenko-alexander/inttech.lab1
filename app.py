from flask import Flask
from config import Configuration
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

app = Flask(__name__)
app.config.from_object(Configuration)
db = SQLAlchemy(app)
login_manager = LoginManager(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)
