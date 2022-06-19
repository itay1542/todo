from flask import Flask
from flask_restful import Api

from config import get_configuration
from src.api.resources.auth_resource import AuthStore

from .api.resources import AuthResource, TodoResource, TodosResource
from .data_access.database import db, db_session
from .middleware.todo_store import TodoStore


def build_app():
    app = Flask(__name__)
    _load_config(app)
    _load_resources(app)
    db.init_app(app)
    with app.app_context():
        db.create_all()
    return app


def _load_resources(app):
    api = Api(app)
    api.add_resource(
        AuthResource,
        "/auth",
        resource_class_kwargs={"auth_store": AuthStore(db_session=db_session)},
    )
    api.add_resource(
        TodosResource,
        "/todos",
        resource_class_kwargs={"todo_store": TodoStore(db_session=db_session)},
    )
    api.add_resource(
        TodoResource,
        "/todo/<int:id>",
        resource_class_kwargs={"todo_store": TodoStore(db_session=db_session)},
    )


def _load_config(app):
    app.config.from_object(get_configuration())
