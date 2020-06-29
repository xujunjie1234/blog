from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate

import pymysql
pymysql.install_as_MySQLdb()


db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()