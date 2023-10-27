from flask import Flask
app = Flask(__name__)

from config import Config
app.config.from_object(Config)

from .models import db, User
db.init_app(app)


from flask_migrate import Migrate
migrate = Migrate(app, db)

from flask_login import LoginManager
from flask_moment import Moment
login_manager = LoginManager(app)
moment = Moment(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).first()

login_manager.login_view = 'login'
login_manager.login_message = 'Please log in to access this page!'
login_manager.login_message_category = 'danger'

from . import routes
