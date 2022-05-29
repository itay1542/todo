from flask import current_app


def get_config():
    # this is used to decouple the program from flask
    return current_app.config
