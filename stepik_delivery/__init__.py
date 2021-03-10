from flask import Flask
from flask_migrate import Migrate

from stepik_delivery.config import Config
from stepik_delivery.models import db

migrate = Migrate()
app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
migrate.init_app(app, db)

from stepik_delivery.views import *
