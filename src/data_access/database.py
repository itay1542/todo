from flask_sqlalchemy import SQLAlchemy
from werkzeug.local import LocalProxy

db = SQLAlchemy()
db_session = LocalProxy(lambda: db.session)