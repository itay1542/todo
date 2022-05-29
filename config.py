class BaseConfig:
    SERVER_BIND_IP = "0.0.0.0"
    SERVER_BIND_PORT = 8080

    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:postgres@localhost:5432/aqua_todo"

    AUTH_COOKIE_KEY = "user_id"
    DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"

def get_configuration() -> type(BaseConfig):
    return BaseConfig()